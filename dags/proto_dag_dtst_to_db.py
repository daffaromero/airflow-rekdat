# !! ATTENTION !!
# 1. Download the dataset of sentiment140 (https://www.kaggle.com/datasets/kazanova/sentiment140)
# 2. Add "target, twitId, date, flag, userName, twitContent" in the first row of the CSV for headers

import psycopg2 as pg
import psycopg2.extras as extras
import pandas as pd

def dag():
    conn = pg.connect("host=localhost dbname=pycsv user=postgres password=admin")
    
    # Fetch data from CSV of some rows and updates the CSV
    path = 'sentiment140.csv'                                           # Specify the file path of Sentiment140 CSV dataset
    num_of_rows = 10                                                    
    
    df_all = pd.read_csv(path, encoding='latin-1')
    dfres = df_all.head(num_of_rows)                                    # Get the row of 0-{num_of_rows} data
    df_all.drop(df_all.index[0:num_of_rows], axis=0, inplace=True)      # Get the row of {num_of_rows}-end data
    df_all.to_csv("sentiment140.csv", index=False)                      # Update CSV file with sliced dataframe
    
    # Dropping irrelevant attributes
    df = dfres.drop(['target', 'date', 'flag'], axis=1)
    
    # Adding to PostgreSQL  
    tuples = [tuple(x) for x in df.to_numpy()]
    tablename = 'sentiment_dataset'
  
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
    
dag() # For each dag() called, we will be pushing 10 first rows to the database