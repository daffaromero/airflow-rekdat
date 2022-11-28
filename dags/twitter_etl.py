import tweepy
import pandas as pd
import json
from datetime import datetime


local_filepath = f"../data/tweets.csv"


def run_twitter_etl():

    # Twitter authentication
    consumer_key = 'xxhLZKqGabwbTAFU7WHPDa5Jl'
    consumer_secret = 'S3ir9SCmtThwqKyEcaFmZIXiaI1aC5BGImO8BBrJNtvGoqHiEO'
    access_key = '914125130946682880-a02PuQgJAfdYZsigqf8a9ppYY8vIgvG'
    access_secret = 'LG6OIGgezptevbdNbJdZPYmbEhooCGcji9R7bLlevQlOI'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    hashtag = '#WorldCup'
    query = tweepy.Cursor(api.search_tweets, q=hashtag,
                          tweet_mode='extended').items(100)
    # print(tweets)

    list = []
    for tweet in query:
        if 'retweeted_status' in tweet._json:
            text = tweet._json['retweeted_status']["full_text"]
        else:
            text = tweet.full_text

        refined_tweet = {"user": tweet.user.screen_name,
                         'text': text,
                         'created_at': tweet.created_at}

        list.append(refined_tweet)

    df = pd.DataFrame(list)
    # df.to_csv(r'C:\Users\daffa\docker\airflow\refined_tweets.csv')
