import os
from dotenv import load_dotenv
# python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of application
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

# below reads variables from the .env file and sets them in os.environ
load_dotenv()

# custom function 
def get_snowflake_engine():
    engine = create_engine(
        URL(
            account=os.getenv("SF_ACCOUNT"),
            user=os.getenv("SF_USER"),
            password=os.getenv("SF_PW"),
            role=os.getenv("SF_ROLE"),
            warehouse=os.getenv("SF_WAREHOUSE"),
            database=os.getenv("SF_DATABASE"),
            schema=os.getenv("SF_SCHEMA")
        )
    )
    return engine

def load_data_to_snowflake(df, table_name):
    engine = get_snowflake_engine()
    try:
        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)
            print(f"Data loaded successfully into Snowflake table: {table_name}")
    except Exception as e:
        print(f"Error occurred while loading data into Snowflake table: {table_name}")
        print(f"Error message: {str(e)}")
    finally:
        engine.dispose()
