import tweepy
from pandas import pandas as pd
import csv
from pathlib import Path
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

consumer_key = 'xxhLZKqGabwbTAFU7WHPDa5Jl'
consumer_secret = 'S3ir9SCmtThwqKyEcaFmZIXiaI1aC5BGImO8BBrJNtvGoqHiEO'
access_key = '914125130946682880-a02PuQgJAfdYZsigqf8a9ppYY8vIgvG'
access_secret = 'LG6OIGgezptevbdNbJdZPYmbEhooCGcji9R7bLlevQlOI'

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
    'twitter_crawl',
    default_args=default_args,
    description='twitter crawling DAG',
    schedule_interval=timedelta(days=1),
)


def get_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_data_search(**kwargs):
    data = []
    query = "#WorldCup"
    api = get_auth()
    cursor = tweepy.Cursor(api.search_tweets, result_type='mixed',
                           q=query, include_entities=True).items(100)
    c = 0
    for x in cursor:
        c = c + 1
        print(x)
        data.append(x)
        if c == 100:
            break
    return data


def parse_data(**context):
    all_data = []
    value = context['task_instance'].xcom_pull(task_ids='crawling_data')
    for tweet in value:
        print(tweet)
        dict_line = {
            "createdAt": str(tweet.created_at),
            "twitId": tweet.id,
            "twitContent": str(tweet.text.encode('ascii', 'ignore').decode("ascii")),
            "userId": tweet.user.id,
            # tweet.user.name.encode('ascii', 'ignore').decode("ascii"),
            "userName": tweet.user.screen_name,
            "location": tweet.user.location,
            "retweet": tweet.retweet_count,
            "like": tweet.favorite_count,
            "userImg": tweet.user.profile_image_url_https,
            "tag": "",
            "type": "",
                    "profile": tweet.user.profile_image_url_https,
                    "screen_name": tweet.user.screen_name,
                    "description": tweet.user.description,
                    "url": tweet.user.url,
                    "followers_count": tweet.user.followers_count,
                    "friends_count": tweet.user.friends_count,
                    "protected": tweet.user.protected,
                    "listed_count": tweet.user.listed_count,
                    "created_at": str(tweet.user.created_at),
                    "verified": tweet.user.verified,
                    "statuses_count": tweet.user.statuses_count,
        }
        all_data.append(dict_line)
    return all_data


csv_path = Path("/opt/airflow/data/tweets_crawl.csv")


def save_data(**kwargs):
    # Xcoms to get the list
    ti = kwargs['ti']
    value = ti.xcom_pull(task_ids='parsing_data')
    df = pd.DataFrame(value)

    try:
        print(df)
        df.to_csv(csv_path, index=False, header=True)
        return True
    except OSError as e:
        print(e)
        return False


t1 = PythonOperator(
    task_id='crawling_data',
    python_callable=get_data_search,
    # provide_context=True,
    dag=dag)

t2 = PythonOperator(
    task_id='parsing_data',
    python_callable=parse_data,
    provide_context=True,
    dag=dag)
t3 = PythonOperator(
    task_id='save_data',
    python_callable=save_data,
    provide_context=True,
    dag=dag)

t1 >> t2 >> t3
