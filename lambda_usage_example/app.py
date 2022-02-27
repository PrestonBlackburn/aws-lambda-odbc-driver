
import json
import io
import os
import pyodbc
import boto3
import pandas as pd


def lambda_handler(event, context):

    print("---lambda started---")

    TEST = False

    #### Credentials ####

    #Azure SQL Server
    host = "your-database.database.windows.net"
    database= "your-database"
    username="username"
    password="password"
    driver = "{ODBC Driver 17 for SQL Server}"

    #AWS S3 Location
    s3 = boto3.client('s3')
    bucket = 'your-bucket-name'


    #### Read Data ####
    print("Available Drivers: ", pyodbc.drivers())
    conx_string = f"driver={driver}; server={host}; \
                    database={database}; UID={username}; PWD={password}"
    conx = pyodbc.connect(conx_string)

    if TEST == True:
        query_tables = "SELECT * FROM information_schema.tables;"
        df_tables = pd.read_sql(query_tables, conx)

        tables = "testing:  " + str(df_tables.iloc[:,2].values)
        print(tables)
        conx.close()

    else:
        query_tables = "SELECT * FROM information_schema.tables;"
        df_tables = pd.read_sql(query_tables, conx)

        tables = str(df_tables.iloc[:,2].values)
        print(tables)
        conx.close()


    #### Save To S3 ####
    tables_file = 'database_tables.csv'


    if TEST == True:
        csv_buffer = io.StringIO()
        df_tables.to_csv(csv_buffer, index=False)

        try:
            s3.put_object(Bucket=bucket, Key = tables_file, Body = csv_buffer.getvalue())
            print("put complete")

        except:
            print("could not upload csv files")


    else:
        files_list = [tables_file]
        df_list = [df_tables]

        for file in range(len(files_list)):
            csv_buffer = io.StringIO()
            df_list[file].to_csv(csv_buffer, index=False)

            try:
                s3.put_object(Bucket=bucket, Key = files_list[file], Body = csv_buffer.getvalue())
                print(f"put {files_list[file]} complete")

            except:
                print(f"could not upload {files_list[file]} files")


    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "tables": tables,
            }
        ),
    }