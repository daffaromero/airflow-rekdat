# !! ATTENTION !!
# 1. Download the dataset of sentiment140 (https://www.kaggle.com/datasets/kazanova/sentiment140)
# 2. Add "training.1600000.processed.noemoticon.csv" in the first row of the CSV for headers

import psycopg2 as pg
import psycopg2.extras as extras
import pandas as pd
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['email@mail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'csv_to_azure',
    default_args=default_args,
    description='load csv to databse DAG',
    schedule_interval=timedelta(days=1),
)

# Update connection string information
host = "twitter-sentiment-analysis.postgres.database.azure.com"
dbname = "twitter"
user = "rekdat"
password = "kelompok11!"
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(
    host, user, dbname, password, sslmode)
print("Connection established")


def csv_to_db():
    conn = pg.connect(conn_string)

    # Fetch data from CSV of some rows and updates the CSV
    # Specify the file path of Sentiment140 CSV dataset
    path = '/opt/airflow/data/sentiment140.csv'
    num_of_rows = 100

    df_all = pd.read_csv(path, encoding='latin-1')
    # Get the row of 0-{num_of_rows} data
    dfres = df_all.head(num_of_rows)
    # Get the row of {num_of_rows}-end data
    df_all.drop(df_all.index[0:num_of_rows], axis=0, inplace=True)
    # Update CSV file with sliced dataframe
    df_all.to_csv(path, index=False)

    # Dropping irrelevant attributes
    df = dfres.drop(['target', 'date', 'flag'], axis=1)

    # Adding to PostgreSQL
    tuples = [tuple(x) for x in df.to_numpy()]
    tablename = 'tweet_kaggle'

    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (tablename, cols)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS """ + tablename + """ (
                twitId varchar(100),
                twitContent varchar(500),
                userName varchar(50)
            );
        """)
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()


task1 = PythonOperator(
    task_id='csv-azure',
    python_callable=csv_to_db,
    provide_context=True,
    dag=dag)

task1
