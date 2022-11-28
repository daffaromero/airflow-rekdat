# -*- coding: utf-8 -*-
"""Copy of Twitter Sentiment Analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_5-5RwCiwE8oup5tMHEVL_cqSWcCc9Ws

# **Get Data**
Get Data from twitter using tweepy and integrated with Twitter Developer Portal to get the API token.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install tweepy==4.6.0

from tweepy import *

import tweepy
import csv
import re 
import string
 
consumer_key = 'wuPuP6lccKSuqDk7AUEDvHi26'
consumer_secret = 'yf76kho0nqNayOKeQv7QBmhFmPpwOj8FLIfCk3rsnFew9J9Orp'
access_key = '1576493200138567681-kAiUnsBg73TncO8kGdBIjMx30k0VTL'
access_secret = '7vYWn2B4vWfMp3R7Pc3cipD0Nh0pUOOaNvkbR4KN9Aor5'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)
 
# csvFile = open('test', 'a')
# csvWriter = csv.writer(csvFile)
 
# search_words = "#palestine"      # enter your words
# new_search = search_words + " -filter:retweets"
 
# for tweet in tweepy.Cursor(api.search_tweets,q=new_search,count=100,
#                            lang="en",
#                            since_id=0).items():
#     csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.user.screen_name.encode('utf-8'), tweet.user.location.encode('utf-8')])

hashtag = '#IranProtests'
query = tweepy.Cursor(api.search_tweets, q=hashtag).items(1000)
tweets = [{'Tweets': tweet.text, 'Timestamp':tweet.created_at} for tweet in query]
print(tweets)

import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

df = pd.DataFrame.from_dict(tweets)

df.head()

df.info()

df.isnull().sum()

df.columns

text_df = df.drop(['Timestamp'], axis=1)
text_df.head()

print(text_df['Tweets'].iloc[0],"\n")
print(text_df['Tweets'].iloc[1],"\n")
print(text_df['Tweets'].iloc[2],"\n")
print(text_df['Tweets'].iloc[3],"\n")
print(text_df['Tweets'].iloc[4],"\n")

text_df.info()

def data_processing(text):
    text = text.lower()
    text = re.sub(r"https\S+|www\S+https\S+", '',text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','',text)
    text = re.sub(r'[^\w\s]','',text)
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w in stop_words]
    return " ".join(filtered_text)

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
text_df.text = text_df['Tweets'].apply(data_processing)

text_df = text_df.drop_duplicates('Tweets')

stemmer = PorterStemmer()
def stemming(data):
    text = [stemmer.stem(word) for word in data]
    return data

text_df['Tweets'] = text_df['Tweets'].apply(lambda x: stemming(x))

text_df.head()

print(text_df['Tweets'].iloc[0],"\n")
print(text_df['Tweets'].iloc[1],"\n")
print(text_df['Tweets'].iloc[2],"\n")
print(text_df['Tweets'].iloc[3],"\n")
print(text_df['Tweets'].iloc[4],"\n")

text_df.info()

def polarity(text):
    return TextBlob(text).sentiment.polarity

text_df['polarity'] = text_df['Tweets'].apply(polarity)

text_df.head(10)

def sentiment(label):
    if label <0:
        return "Negative"
    elif label ==0:
        return "Neutral"
    elif label>0:
        return "Positive"

text_df['sentiment'] = text_df['polarity'].apply(sentiment)

text_df.head()

fig = plt.figure(figsize=(5,5))
sns.countplot(x='sentiment', data = text_df)

fig = plt.figure(figsize=(7,7))
colors = ("yellowgreen", "gold", "red")
wp = {'linewidth':2, 'edgecolor':"black"}
tags = text_df['sentiment'].value_counts()
explode = (0.1,0.1,0.1)
tags.plot(kind='pie', autopct='%1.1f%%', shadow=True, colors = colors,
         startangle=90, wedgeprops = wp, explode = explode, label='')
plt.title('Distribution of sentiments')

pos_tweets = text_df[text_df.sentiment == 'Positive']
pos_tweets = pos_tweets.sort_values(['polarity'], ascending= False)
pos_tweets.head()

text = ' '.join([word for word in pos_tweets['Tweets']])
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in positive tweets', fontsize=19)
plt.show()

neg_tweets = text_df[text_df.sentiment == 'Negative']
neg_tweets = neg_tweets.sort_values(['polarity'], ascending= False)
neg_tweets.head()

text = ' '.join([word for word in neg_tweets['Tweets']])
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in negative tweets', fontsize=19)
plt.show()

neutral_tweets = text_df[text_df.sentiment == 'Neutral']
neutral_tweets = neutral_tweets.sort_values(['polarity'], ascending= False)
neutral_tweets.head()

text = ' '.join([word for word in neutral_tweets['Tweets']])
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in neutral tweets', fontsize=19)
plt.show()

vect = CountVectorizer(ngram_range=(1,2)).fit(text_df['Tweets'])

feature_names = vect.get_feature_names()
print("Number of features: {}\n".format(len(feature_names)))
print("First 20 features:\n {}".format(feature_names[:20]))

X = text_df['Tweets']
Y = text_df['sentiment']
X = vect.transform(X)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Size of x_train:", (x_train.shape))
print("Size of y_train:", (y_train.shape))
print("Size of x_test:", (x_test.shape))
print("Size of y_test:", (y_test.shape))

import warnings
warnings.filterwarnings('ignore')

logreg = LogisticRegression()
logreg.fit(x_train, y_train)
logreg_pred = logreg.predict(x_test)
logreg_acc = accuracy_score(logreg_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, logreg_pred))
print("\n")
print(classification_report(y_test, logreg_pred))

style.use('classic')
cm = confusion_matrix(y_test, logreg_pred, labels=logreg.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=logreg.classes_)
disp.plot()

from sklearn.model_selection import GridSearchCV

param_grid={'C':[0.001, 0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid)
grid.fit(x_train, y_train)

print("Best parameters:", grid.best_params_)

y_pred = grid.predict(x_test)

logreg_acc = accuracy_score(y_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

from sklearn.svm import LinearSVC

SVCmodel = LinearSVC()
SVCmodel.fit(x_train, y_train)

svc_pred = SVCmodel.predict(x_test)
svc_acc = accuracy_score(svc_pred, y_test)
print("test accuracy: {:.2f}%".format(svc_acc*100))

print(confusion_matrix(y_test, svc_pred))
print("\n")
print(classification_report(y_test, svc_pred))

grid = {
    'C':[0.01, 0.1, 1, 10],
    'kernel':["linear","poly","rbf","sigmoid"],
    'degree':[1,3,5,7],
    'gamma':[0.01,1]
}
grid = GridSearchCV(SVCmodel, param_grid)
grid.fit(x_train, y_train)

print("Best parameter:", grid.best_params_)

y_pred = grid.predict(x_test)

logreg_acc = accuracy_score(y_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

"""Additional code to extract data form twitter using twitter api"""

import tweepy #to access the twitter api
import pandas as pd #for basic data operations

# Importing the keys from twitter api
consumerKey = "xxxxxxxxxxxxxxxxxxxx"
consumerSecret = "xxxxxxxxxxxxxxxxxxxx"
accessToken = "xxxxxxxxxxxxxxxxxxxx"
accessTokenSecret = "xxxxxxxxxxxxxxxxxxxx"

# Establish the connection with twitter API
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# Search for the Term and define number of tweets 
searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms = int(input("Enter how many tweets to search: "))

# Get no of tweets and searched term together 
tweets = tweepy.Cursor(api.search_tweets, q=searchTerm).items(NoOfTerms)
