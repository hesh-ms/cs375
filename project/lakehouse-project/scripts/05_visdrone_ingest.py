from pathlib import Path
import subprocess

import boto3
import imageio_ffmpeg
import pandas as pd


# ----------------------------
# CONFIG
# ----------------------------

BUCKET = "lakehouse"
S3_ENDPOINT = "http://rustfs:9000"

DATASET_ROOT = Path(
    "/workspace/data/visdrone/VisDrone2019-VID-val"
)

SEQUENCES = [
    "uav0000086_00000_v",
    "uav0000117_02622_v",
    "uav0000137_00458_v",
]

FPS = 30
FRAGMENT_FRAMES = 30  # 1-second fragments at 30 fps

LOCAL_FRAGMENT_ROOT = Path("/data/local/visdrone_fragments")
LOCAL_FRAGMENT_ROOT.mkdir(parents=True, exist_ok=True)

CATEGORY_NAMES = {
    0: "ignored",
    1: "pedestrian",
    2: "person",
    3: "bicycle",
    4: "car",
    5: "van",
    6: "truck",
    7: "tricycle",
    8: "awning-tricycle",
    9: "bus",
    10: "motor",
    11: "others",
}


# ----------------------------
# CONNECTIONS
# ----------------------------

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfsadmin",
)

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


# ----------------------------
# HELPERS
# ----------------------------

def parse_annotations(sequence_name):
    """
    Parse one VisDrone VID ground-truth file.

    Columns:
    frame_index,target_id,bbox_left,bbox_top,bbox_width,bbox_height,
    score,object_category,truncation,occlusion
    """
    annotation_path = DATASET_ROOT / "annotations" / f"{sequence_name}.txt"

    df = pd.read_csv(
        annotation_path,
        header=None,
        names=[
            "frame_index",
            "target_id",
            "bbox_left",
            "bbox_top",
            "bbox_width",
            "bbox_height",
            "score",
            "category_id",
            "truncation",
            "occlusion",
        ],
    )

    df["sequence_id"] = sequence_name
    df["category"] = df["category_id"].map(CATEGORY_NAMES).fillna("unknown")

    # Keep all annotations in raw. The fragment statistics below count only
    # evaluation-valid objects in the 10 target classes.
    return df


def sequence_frame_numbers(sequence_name):
    sequence_dir = DATASET_ROOT / "sequences" / sequence_name
    frames = sorted(sequence_dir.glob("*.jpg"))

    if not frames:
        raise RuntimeError(f"No frames found for {sequence_name}")

    return [int(frame.stem) for frame in frames]


def encode_fragment(sequence_name, start_frame, end_frame, fragment_id):
    """
    Encode a short fragmented MP4 from the JPEG frame sequence.
    """
    sequence_dir = DATASET_ROOT / "sequences" / sequence_name
    output_dir = LOCAL_FRAGMENT_ROOT / sequence_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"fragment_{fragment_id:04d}.mp4"
    frame_count = end_frame - start_frame + 1

    command = [
        ffmpeg,
        "-y",
        "-loglevel", "error",
        "-framerate", str(FPS),
        "-start_number", str(start_frame),
        "-i", str(sequence_dir / "%07d.jpg"),
        "-frames:v", str(frame_count),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        str(output_path),
    ]

    subprocess.run(command, check=True)

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(f"Failed to create {output_path}")

    return output_path


def upload_fragment(sequence_name, fragment_id, local_path):
    key = (
        f"assets/visdrone/{sequence_name}/"
        f"fragment_{fragment_id:04d}.mp4"
    )

    with local_path.open("rb") as f:
        s3.upload_fileobj(
            f,
            BUCKET,
            key,
            ExtraArgs={"ContentType": "video/mp4"},
        )

    return f"s3://{BUCKET}/{key}"


# ----------------------------
# INGEST THREE VID SEQUENCES
# ----------------------------

all_annotations = []
fragment_rows = []

for sequence_name in SEQUENCES:
    print(f"\nProcessing {sequence_name}")

    annotations = parse_annotations(sequence_name)
    all_annotations.append(annotations)

    frame_numbers = sequence_frame_numbers(sequence_name)

    min_frame = min(frame_numbers)
    max_frame = max(frame_numbers)

    print(
        f"  frames: {len(frame_numbers)} "
        f"({min_frame}..{max_frame})"
    )
    print(f"  raw annotation rows: {len(annotations)}")

    fragment_id = 0

    for start_frame in range(
        min_frame,
        max_frame + 1,
        FRAGMENT_FRAMES,
    ):
        end_frame = min(
            start_frame + FRAGMENT_FRAMES - 1,
            max_frame,
        )

        # Make sure this fragment is a contiguous range of existing frames.
        expected = set(range(start_frame, end_frame + 1))
        existing = set(frame_numbers)

        if not expected.issubset(existing):
            print(
                f"  skipping fragment {fragment_id}: "
                "missing source frames"
            )
            fragment_id += 1
            continue

        fragment_ann = annotations[
            (annotations["frame_index"] >= start_frame)
            & (annotations["frame_index"] <= end_frame)
        ]

        valid_objects = fragment_ann[
            (fragment_ann["score"] == 1)
            & (fragment_ann["category_id"].between(1, 10))
        ]

        local_path = encode_fragment(
            sequence_name,
            start_frame,
            end_frame,
            fragment_id,
        )

        fragment_uri = upload_fragment(
            sequence_name,
            fragment_id,
            local_path,
        )

        classes = sorted(valid_objects["category"].dropna().unique().tolist())

        fragment_rows.append(
            {
                "sequence_id": sequence_name,
                # Logical clip prefix. Individual bytes are in fragment_uri.
                "clip_uri": (
                    f"s3://{BUCKET}/assets/visdrone/"
                    f"{sequence_name}/"
                ),
                "fragment_uri": fragment_uri,
                "fragment_id": fragment_id,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": (start_frame - 1) / FPS,
                "end_time": end_frame / FPS,
                "n_objects": int(len(valid_objects)),
                "classes": ",".join(classes),
                "fps": FPS,
            }
        )

        print(
            f"  fragment {fragment_id:04d}: "
            f"frames {start_frame}-{end_frame}, "
            f"objects={len(valid_objects)}"
        )

        fragment_id += 1


# ----------------------------
# STAGE PARQUET METADATA
# ----------------------------

annotations_df = pd.concat(all_annotations, ignore_index=True)
fragments_df = pd.DataFrame(fragment_rows)

annotations_path = Path(
    "/data/local/visdrone_annotations_raw.parquet"
)
fragments_path = Path(
    "/data/local/visdrone_fragments_raw.parquet"
)

annotations_df.to_parquet(annotations_path, index=False)
fragments_df.to_parquet(fragments_path, index=False)

print("\nVISDRONE INGESTION COMPLETE")
print("----------------------------")
print("Sequences:", len(SEQUENCES))
print("Annotation rows:", len(annotations_df))
print("Fragments:", len(fragments_df))
print("Total indexed objects:", int(fragments_df["n_objects"].sum()))

print("\nTop 10 busiest fragments:")
print(
    fragments_df[
        [
            "sequence_id",
            "fragment_id",
            "start_frame",
            "end_frame",
            "n_objects",
            "fragment_uri",
        ]
    ]
    .sort_values("n_objects", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\nStaged:")
print(annotations_path)
print(fragments_path)
