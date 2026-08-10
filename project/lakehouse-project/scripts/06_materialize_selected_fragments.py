from pathlib import Path
from urllib.parse import urlparse

import boto3
import duckdb

S3_ENDPOINT = "http://rustfs:9000"
OUTPUT_DIR = Path("/data/local/selected_fragments")
LIMIT = 10

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())

# Query metadata first
selected = con.sql(f"""
SELECT
    fragment_uri,
    sequence_id,
    fragment_id,
    start_frame,
    end_frame,
    n_objects
FROM silver.visdrone_fragments
WHERE n_objects > 20
ORDER BY n_objects DESC
LIMIT {LIMIT}
""").df()

print("SELECTED FRAGMENTS")
print(selected.to_string(index=False))

# Materialize only the selected objects
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfsadmin",
)

downloaded = []

for row in selected.itertuples(index=False):
    parsed = urlparse(row.fragment_uri)

    bucket = parsed.netloc
    key = parsed.path.lstrip("/")

    filename = (
        f"{row.sequence_id}_fragment_"
        f"{int(row.fragment_id):04d}.mp4"
    )

    destination = OUTPUT_DIR / filename

    s3.download_file(
        bucket,
        key,
        str(destination),
    )

    downloaded.append({
        "path": str(destination),
        "bytes": destination.stat().st_size,
        "n_objects": int(row.n_objects),
    })

print("\nMATERIALIZED ONLY SELECTED FRAGMENTS")
print("------------------------------------")
print("Selected by DuckDB:", len(selected))
print("Downloaded from RustFS:", len(downloaded))
print("Destination:", OUTPUT_DIR)

for item in downloaded:
    print(
        f"{item['path']} | "
        f"{item['bytes']} bytes | "
        f"{item['n_objects']} objects"
    )