CREATE OR REPLACE TABLE silver.coco_annotations AS
SELECT DISTINCT
    image_id,
    image_uri,
    bbox_id,
    category_id,
    category,
    CAST(bbox_xmin AS DOUBLE) AS bbox_xmin,
    CAST(bbox_ymin AS DOUBLE) AS bbox_ymin,
    CAST(bbox_xmax AS DOUBLE) AS bbox_xmax,
    CAST(bbox_ymax AS DOUBLE) AS bbox_ymax,
    CAST(area AS DOUBLE) AS area,
    split
FROM raw.coco_annotations
WHERE image_uri IS NOT NULL
  AND category IS NOT NULL
  AND bbox_xmax > bbox_xmin
  AND bbox_ymax > bbox_ymin;


CREATE OR REPLACE TABLE silver.visdrone_fragments AS
SELECT DISTINCT
    sequence_id,
    clip_uri,
    fragment_uri,
    fragment_id,
    CAST(start_frame AS BIGINT) AS start_frame,
    CAST(end_frame AS BIGINT) AS end_frame,
    CAST(start_time AS DOUBLE) AS start_time,
    CAST(end_time AS DOUBLE) AS end_time,
    CAST(n_objects AS BIGINT) AS n_objects,
    classes,
    CAST(fps AS BIGINT) AS fps
FROM raw.visdrone_fragments
WHERE fragment_uri IS NOT NULL
  AND end_frame >= start_frame
  AND n_objects >= 0;