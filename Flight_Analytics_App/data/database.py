import duckdb as ddb


sql_output = ddb.sql(
    """ select * from '/home/sai/Study/oct28_deliverables/combined.csv' limit 10 """
).fetchall()
