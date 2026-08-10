import datasets
import duckdb

# Hugging Face dataset
ds = datasets.load_dataset(
    "cornell-movie-review-data/rotten_tomatoes",
    split="train[:100]"
)

# Stage locally as Parquet
ds.to_parquet("/data/local/raw_tmp.parquet")

# Attach DuckLake
con = duckdb.connect()
con.execute(open("sql/00_attach.sql").read())

# Raw DuckLake table
con.execute("""
    CREATE OR REPLACE TABLE raw.movie_reviews AS
    SELECT *
    FROM read_parquet('/data/local/raw_tmp.parquet');
""")

print("Raw table:")
print(con.sql("SELECT * FROM raw.movie_reviews LIMIT 5"))

print("\nRow count:")
print(con.sql("SELECT COUNT(*) FROM raw.movie_reviews"))