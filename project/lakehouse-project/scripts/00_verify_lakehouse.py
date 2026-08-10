import duckdb

con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())

print("TABLES")
print(con.sql("SHOW ALL TABLES"))

print("\nRECENT SNAPSHOTS")
print(con.sql("""
SELECT snapshot_id, snapshot_time, schema_version, changes
FROM lake.snapshots()
ORDER BY snapshot_id DESC
LIMIT 10
"""))
