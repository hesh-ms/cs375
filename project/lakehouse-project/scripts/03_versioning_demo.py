import duckdb

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())


before = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

print("BEFORE snapshot:", before)

# ----- Schema evolution -----
columns = {
    row[1]
    for row in con.sql("PRAGMA table_info('silver.coco_annotations')").fetchall()
}

if "bbox_area_calc" not in columns:
    con.execute("""
    ALTER TABLE silver.coco_annotations
    ADD COLUMN bbox_area_calc DOUBLE;
    """)

con.execute("""
UPDATE silver.coco_annotations
SET bbox_area_calc =
    (bbox_xmax - bbox_xmin) * (bbox_ymax - bbox_ymin);
""")

good_snapshot = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

good_time = con.sql(f"""
SELECT snapshot_time
FROM lake.snapshots()
WHERE snapshot_id = {good_snapshot}
""").fetchone()[0]

print("GOOD snapshot:", good_snapshot)
print("GOOD snapshot time:", good_time)

# ----- Deliberately bad transform -----
con.execute("""
DELETE FROM silver.coco_annotations
WHERE category = 'person';
""")

bad_snapshot = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

print("BAD snapshot:", bad_snapshot)
print(
    "Current person rows:",
    con.sql("""
        SELECT COUNT(*)
        FROM silver.coco_annotations
        WHERE category = 'person'
    """).fetchone()[0],
)

# ----- Time travel by version -----
print(
    "Person rows at good VERSION:",
    con.sql(f"""
        SELECT COUNT(*)
        FROM silver.coco_annotations
        AT (VERSION => {good_snapshot})
        WHERE category = 'person'
    """).fetchone()[0],
)

# ----- Time travel by timestamp -----
print(
    "Person rows at good TIMESTAMP:",
    con.sql(f"""
        SELECT COUNT(*)
        FROM silver.coco_annotations
        AT (TIMESTAMP => TIMESTAMPTZ '{good_time}')
        WHERE category = 'person'
    """).fetchone()[0],
)

# ----- Snapshot comparison -----
con.execute("USE lake.silver")

print("\nSNAPSHOT COMPARISON")
print(con.sql(f"""
FROM lake.table_changes(
    'coco_annotations',
    {good_snapshot},
    {bad_snapshot}
)
LIMIT 20
"""))

# ----- Rollback -----
con.execute(f"""
CREATE OR REPLACE TABLE silver.coco_annotations AS
SELECT *
FROM silver.coco_annotations
AT (VERSION => {good_snapshot});
""")

rollback_snapshot = con.sql(
    "SELECT MAX(snapshot_id) FROM lake.snapshots()"
).fetchone()[0]

print("\nROLLBACK COMPLETE")
print("Rollback snapshot:", rollback_snapshot)
print(
    "Person rows after rollback:",
    con.sql("""
        SELECT COUNT(*)
        FROM silver.coco_annotations
        WHERE category = 'person'
    """).fetchone()[0],
)
print(
    "Total rows after rollback:",
    con.sql("""
        SELECT COUNT(*)
        FROM silver.coco_annotations
    """).fetchone()[0],
)
