CREATE OR REPLACE TABLE gold.coco_training AS
SELECT
    image_uri,
    category AS label,
    split,
    COUNT(*) AS n_objects
FROM silver.coco_annotations
GROUP BY image_uri, category, split;

CREATE OR REPLACE TABLE gold.visdrone_training AS
SELECT
    fragment_uri,
    sequence_id,
    fragment_id,
    start_frame,
    end_frame,
    start_time,
    end_time,
    n_objects,
    classes,
    fps
FROM silver.visdrone_fragments
WHERE n_objects > 20;