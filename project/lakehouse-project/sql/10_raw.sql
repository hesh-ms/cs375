CREATE OR REPLACE TABLE raw.coco_images AS
SELECT *
FROM read_parquet('/data/local/coco_images_raw.parquet');

CREATE OR REPLACE TABLE raw.coco_annotations AS
SELECT *
FROM read_parquet('/data/local/coco_annotations_raw.parquet');

CREATE OR REPLACE TABLE raw.visdrone_annotations AS
SELECT *
FROM read_parquet('/data/local/visdrone_annotations_raw.parquet');

CREATE OR REPLACE TABLE raw.visdrone_fragments AS
SELECT *
FROM read_parquet('/data/local/visdrone_fragments_raw.parquet');