import duckdb as ddb


# scheduled - all count of the route
def route_query_scheduled(ddb, parquet_path, month_count, source_airport, dest_airport):

    if month_count == "1":  # also consider in the logic that mount count = start month
        month_count = "2025-06-01"
    elif month_count == "3":
        month_count = "2025-04-01"
    elif month_count == "6":
        month_count = "2025-01-01"
    elif month_count == "12":
        month_count = "2024-06-30"
    elif month_count == "24":
        month_count = "2023-06-30"
    elif month_count == "90":  # max
        month_count = "2018-01-01"

    sql = """
    SELECT count(*) AS route_count
    FROM read_parquet(?)
    WHERE flight_date BETWEEN CAST(? AS DATE) AND '2025-06-30'  -- remember we are hardcoding the end_date (dataset limit)
      AND ORIGIN = ?
      AND DEST = ?
    """
    return ddb.execute(
        sql, [parquet_path, month_count, source_airport, dest_airport]
    ).fetchone()[0]


# if any of the routes were cancelled
def route_query_cancelled(ddb, parquet_path, month_count, source_airport, dest_airport):

    if month_count == "1":  # also consider in the logic that mount count = start month
        month_count = "2025-06-01"
    elif month_count == "3":
        month_count = "2025-04-01"
    elif month_count == "6":
        month_count = "2025-01-01"
    elif month_count == "12":
        month_count = "2024-06-30"
    elif month_count == "24":
        month_count = "2023-06-30"
    elif month_count == "90":  # max
        month_count = "2018-01-01"

    sql = """
    SELECT count(*) AS route_count
    FROM read_parquet(?)
    WHERE flight_date BETWEEN CAST(? AS DATE) AND '2025-06-30'  -- remember we are hardcoding the end_date (dataset limit)
      AND ORIGIN = ?
      AND DEST = ?
      AND CANCELLED = 1
    """
    return ddb.execute(
        sql, [parquet_path, month_count, source_airport, dest_airport]
    ).fetchone()[0]


# just straight up delayed routes
def route_query_delayed(ddb, parquet_path, month_count, source_airport, dest_airport):

    if month_count == "1":  # also consider in the logic that mount count = start month
        month_count = "2025-06-01"
    elif month_count == "3":
        month_count = "2025-04-01"
    elif month_count == "6":
        month_count = "2025-01-01"
    elif month_count == "12":
        month_count = "2024-06-30"
    elif month_count == "24":
        month_count = "2023-06-30"
    elif month_count == "90":  # max
        month_count = "2018-01-01"

    sql = """
    SELECT count(*) AS route_count
    FROM read_parquet(?)
    WHERE flight_date BETWEEN CAST(? AS DATE) AND '2025-06-30'  -- remember we are hardcoding the end_date (dataset limit)
      AND ORIGIN = ?
      AND DEST = ?
      AND CANCELLED = 0
      AND ARR_DELAY > 15
    """
    return ddb.execute(
        sql, [parquet_path, month_count, source_airport, dest_airport]
    ).fetchone()[0]


# delayed over 15min due to weather
def route_query_weather_delayed(
    ddb, parquet_path, month_count, source_airport, dest_airport
):

    if month_count == "1":  # also consider in the logic that mount count = start month
        month_count = "2025-06-01"
    elif month_count == "3":
        month_count = "2025-04-01"
    elif month_count == "6":
        month_count = "2025-01-01"
    elif month_count == "12":
        month_count = "2024-06-30"
    elif month_count == "24":
        month_count = "2023-06-30"
    elif month_count == "90":  # max
        month_count = "2018-01-01"

    sql = """
    SELECT count(*) AS route_count
    FROM read_parquet(?)
    WHERE flight_date BETWEEN CAST(? AS DATE) AND '2025-06-30'  -- remember we are hardcoding the end_date (dataset limit)
      AND ORIGIN = ?
      AND DEST = ?
      AND CANCELLED = 0
      AND WEATHER_DELAY > 15
    """
    return ddb.execute(
        sql, [parquet_path, month_count, source_airport, dest_airport]
    ).fetchone()[0]
