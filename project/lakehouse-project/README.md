# AI Lakehouse Project

This is my lakehouse project using DuckDB/DuckLake with RustFS for object storage. I used COCO for the image dataset and VisDrone for the video dataset.

The main idea is that the large image/video files stay in RustFS, while DuckLake stores the metadata, annotations, URIs, and version history. I organized the data into raw, silver, and gold layers.

## What I used
DuckDB / DuckLake
RustFS
Docker Compose
Hugging Face datasets
COCO
VisDrone2019-VID

## Datasets

### COCO

I used a subset of 1,000 COCO validation images.

Results:
1,000 images
7,266 object annotations
image files stored under s3://lakehouse/assets/coco/

The DuckLake tables store the image URI, labels, bounding boxes, dimensions, and other metadata instead of storing the image bytes directly.

### VisDrone

I used three sequences from the VisDrone2019 Task 2 VID validation set:
uav0000086_00000_v
uav0000117_02622_v
uav0000137_00458_v

Results:
66,701 annotation rows
36 one-second video fragments
fragments stored under s3://lakehouse/assets/visdrone/

## Setup

The VisDrone validation set should be extracted here:

data/visdrone/VisDrone2019-VID-val/

It should contain the annotations/ and sequences/ folders.

The project .env contains the Hugging Face settings:

HF_TOKEN=hf_your_token_here
HF_REPO=hms6/lakehouse-coco-gold

The real token is not committed to Git.

## Running the project

Start the containers:

docker compose up -d

The RustFS console is available at:

http://localhost:9001

For this project I used:

username: rustfsadmin
password: rustfsadmin

To rebuild the main lakehouse pipeline:

chmod +x rebuild.sh
./rebuild.sh

The rebuild script starts the containers, installs the needed Python packages, makes sure the lakehouse bucket exists, runs the COCO and VisDrone ingestion, and rebuilds the raw, silver, and gold tables.

## Raw, silver, and gold

The raw layer contains the ingested metadata.

Examples:

raw.coco_images
raw.coco_annotations
raw.visdrone_annotations
raw.visdrone_fragments

The silver layer cleans and normalizes the data. For example, the COCO silver table removes invalid rows, deduplicates data, and makes sure the bounding box fields have the right types.

The gold layer contains smaller tables that are easier to use for ML/training tasks.

Examples:

gold.coco_training
gold.visdrone_training

## COCO query

One query I used was to find images with a lot of people:

SELECT image_uri, COUNT(*) AS n_people
FROM silver.coco_annotations
WHERE category = 'person'
GROUP BY image_uri
HAVING COUNT(*) >= 5
ORDER BY n_people DESC;

In my 1,000-image subset there were 2,272 person annotations. The highest count I found in one image was 14.

The saved script for the COCO results is:

docker compose exec lab python scripts/04_coco_evidence.py

## VisDrone fragment query

For VisDrone I split the sequences into one-second fragments and stored metadata about each fragment in DuckLake.

I used this query to find the busiest fragments:

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
LIMIT 10;

Then I used this script to download only the fragments returned by the query:

docker compose exec lab python scripts/06_materialize_selected_fragments.py

The result was:

Selected by DuckDB: 10
Downloaded from RustFS: 10

This lets me query the metadata first and only fetch the video fragments I actually need.

## Versioning

I also tested DuckLake's snapshot/versioning features.

The demo includes:
schema evolution
snapshots
time travel by version
time travel by timestamp
snapshot comparison
a deliberately bad transform
rollback

The script is:

docker compose exec lab python scripts/03_versioning_demo.py

One run of the demo produced:

good snapshot: 16
bad snapshot: 17
person rows after bad transform: 0
person rows from the good snapshot: 2272
rollback snapshot: 18
person rows after rollback: 2272

The exact snapshot numbers can change if the scripts are run again.

## Hugging Face round trip

I also exported the COCO gold table back to Hugging Face.

The script is:

docker compose exec lab python scripts/07_hf_roundtrip.py

Published dataset:

https://huggingface.co/datasets/hms6/lakehouse-coco-gold

## Report

The report/ folder contains the results and screenshots I used for the final report, including the COCO counts, query results, versioning/rollback output, and VisDrone fragment results.
