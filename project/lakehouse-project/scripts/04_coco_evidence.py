import duckdb

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())

print("COCO RAW COUNTS")
print(
    "raw.coco_images:",
    con.sql("SELECT COUNT(*) FROM raw.coco_images").fetchone()[0],
)
print(
    "raw.coco_annotations:",
    con.sql("SELECT COUNT(*) FROM raw.coco_annotations").fetchone()[0],
)

print("\nTOP CATEGORIES")
print(con.sql("""
SELECT category, COUNT(*) AS n
FROM silver.coco_annotations
GROUP BY category
ORDER BY n DESC
LIMIT 15
"""))

print("\nCROWDED SCENES")
print(con.sql("""
SELECT image_uri, COUNT(*) AS n_people
FROM silver.coco_annotations
WHERE category = 'person'
GROUP BY image_uri
HAVING COUNT(*) >= 5
ORDER BY n_people DESC, image_uri
LIMIT 20
"""))

print("\nPERSON-COUNT DISTRIBUTION")
print(con.sql("""
SELECT n_people, COUNT(*) AS n_images
FROM (
    SELECT image_uri, COUNT(*) AS n_people
    FROM silver.coco_annotations
    WHERE category = 'person'
    GROUP BY image_uri
)
GROUP BY n_people
ORDER BY n_people DESC
"""))
