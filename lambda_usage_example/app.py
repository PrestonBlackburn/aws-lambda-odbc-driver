import json
import pyodbc
import pandas as pd
import boto3
import io
import os

def lambda_handler(event, context):

    TEST = True

    #### Credentials ####

    #Azure SQL Server
    host = "hostid.database.windows.net"
    username = "username"
    password = "password"
    database = "database"
    driver = "{ODBC Driver 17 for SQL Server}"

    #AWS S3
    '''
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    '''

    #### Read Data ####

    conx_string = f"driver={driver}; server={host}; \
                    database={database}; UID={username}; PWD={password}"
    conx = pyodbc.connect(conx_string)

    if TEST == True:
        query = "SELECT * FROM information_schema.tables;"
        cursor = conx.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        tables = "testing:  " + str(results)
        print(results)
        conx.close()

    else:
        query_tables = "SELECT * FROM information_schema.tables;"
        df_tables = pd.read_sql(query_tables, conx)
        tables = str(df_tables.iloc[:,2].values)


    #### Save To S3 ####




    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "tables": tables,
            }
        ),
    }
