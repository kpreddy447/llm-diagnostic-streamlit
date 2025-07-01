import os
import pandas as pd

def load_data_from_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found.")
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    return df



# import os
# import pandas as pd
# import psycopg2
# from dotenv import load_dotenv

# def load_data_from_postgres(query, params=None):
#     load_dotenv()

#     host = os.getenv('PG_HOST')
#     port = os.getenv('PG_PORT')
#     database = os.getenv('PG_DATABASE')
#     user = os.getenv('PG_USER')
#     password = os.getenv('PG_PASSWORD')

#     conn = psycopg2.connect(
#         host=host,
#         port=port,
#         database=database,
#         user=user,
#         password=password
#     )

#     df = pd.read_sql_query(query, conn, params=params)
    

#     conn.close()
#     return df

# if __name__ == "__main__":
#     df = load_data_from_postgres("SELECT * FROM public.main_table;")
#     print(df.head())

