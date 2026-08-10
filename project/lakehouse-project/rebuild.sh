#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "== AI Lakehouse rebuild =="

docker compose up -d rustfs lab

echo "Installing Python dependencies..."
docker compose exec -T lab pip install --quiet \
  duckdb datasets huggingface_hub boto3 pyarrow pandas pillow requests \
  jupyter imageio-ffmpeg pytz

echo "Ensuring lakehouse bucket exists..."
docker compose exec -T lab python - <<'PY'
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://rustfs:9000",
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfsadmin",
)

names = [b["Name"] for b in s3.list_buckets()["Buckets"]]
if "lakehouse" not in names:
    s3.create_bucket(Bucket="lakehouse")
    print("Created lakehouse bucket")
else:
    print("lakehouse bucket already exists")
PY

if [[ ! -d "data/visdrone/VisDrone2019-VID-val" ]]; then
  echo "ERROR: expected VisDrone data at data/visdrone/VisDrone2019-VID-val/"
  exit 1
fi

echo "Running COCO ingestion..."
docker compose exec -T lab jupyter nbconvert \
  --to notebook --execute --inplace notebooks/02_coco.ipynb

echo "Running VisDrone ingestion..."
docker compose exec -T lab python scripts/05_visdrone_ingest.py

echo "Building raw/silver/gold..."
docker compose exec -T lab python - <<'PY'
import duckdb

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())
con.execute(open("sql/10_raw.sql").read())
con.execute(open("sql/20_silver.sql").read())
con.execute(open("sql/30_gold.sql").read())

for name in [
    "raw.coco_images",
    "raw.coco_annotations",
    "silver.coco_annotations",
    "gold.coco_training",
    "raw.visdrone_annotations",
    "raw.visdrone_fragments",
    "silver.visdrone_fragments",
    "gold.visdrone_training",
]:
    count = con.sql(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"{name}: {count}")
PY

echo "Rebuild complete."
