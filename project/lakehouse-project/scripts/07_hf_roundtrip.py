import os

import duckdb
from datasets import load_dataset, Dataset


# ----------------------------
# CONFIG
# ----------------------------

HF_REPO = os.environ["HF_REPO"]

# ----------------------------
# 1. Incremental HF ingestion
# ----------------------------

# Small additional HF dataset to demonstrate a new raw snapshot.
ds = load_dataset(
    "cornell-movie-review-data/rotten_tomatoes",
    split="test[:50]",
)

local_path = "/data/local/hf_incremental.parquet"
ds.to_parquet(local_path)

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())

before = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

con.execute("""
CREATE OR REPLACE TABLE raw.hf_incremental AS
SELECT *
FROM read_parquet('/data/local/hf_incremental.parquet');
""")

after = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

print("HF INCREMENTAL INGEST")
print("---------------------")
print("Rows:", len(ds))
print("Snapshot before:", before)
print("Snapshot after:", after)


# ----------------------------
# 2. Export gold COCO table
# ----------------------------

gold_df = con.sql("""
SELECT *
FROM gold.coco_training
ORDER BY image_uri, label
""").df()

gold_path = "/data/local/coco_gold_export.parquet"
gold_df.to_parquet(gold_path, index=False)

print("\nGOLD EXPORT")
print("-----------")
print("Rows:", len(gold_df))
print("Parquet:", gold_path)


# ----------------------------
# 3. Push gold table to HF Hub
# ----------------------------

token = os.environ.get("HF_TOKEN")

if not token:
    raise RuntimeError(
        "HF_TOKEN is not set. Add it to .env before publishing."
    )

hf_ds = Dataset.from_parquet(gold_path)

hf_ds.push_to_hub(
    HF_REPO,
    token=token,
)

print("\nPUBLISHED")
print("---------")
print(f"https://huggingface.co/datasets/{HF_REPO}")
