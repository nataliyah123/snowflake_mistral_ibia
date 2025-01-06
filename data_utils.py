import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import config

def get_snowflake_connection():
    """Establishes and returns a Snowflake connection."""
    conn = snowflake.connector.connect(
        account=config.SNOWFLAKE_ACCOUNT,
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
    )
    return conn

def execute_query(query, conn):
    """Executes a SQL query in Snowflake and returns a pandas DataFrame."""
    try:
      cur = conn.cursor()
      cur.execute(query)
      df = cur.fetch_pandas_all()
      return df
    except Exception as e:
        print(e)
        return pd.DataFrame()
    finally:
      cur.close()

def snowflake_search(query, search_table, conn):
    """
    Performs a semantic search in Snowflake using Cortex Search.
    NOTE: This is using a table name to perform the search
    """
    sql = f"""
        SELECT text, metadata FROM search_index(
            input => '{query}',
            table_name => '{search_table}'
        )
        LIMIT 5;
    """
    return execute_query(sql, conn)

def upload_pandas_to_snowflake(df, table_name, conn):
    """Upload a pandas df to Snowflake"""
    try:
        success, nchunks, nrows, _ = write_pandas(conn, df, table_name)
        print(f"{nrows} Rows uploaded to {table_name}")
        return success
    except Exception as e:
        print(e)
        return False