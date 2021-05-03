import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(10) 

client = pymongo.MongoClient("mongodb")
db = client.tweet_collector

pg = create_engine('postgres://postgres:postgres@postgres:5432/postgres', echo=True)

pg.execute('''
    DROP TABLE IF EXISTS tweets;
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(5000),
    username VARCHAR(50),
    score NUMERIC
);
''')

#Sentiment_analysing

s = SentimentIntensityAnalyzer()

entries = db.tweets.find()
for e in entries:
    text = e['text']
    username = e['username']
    score = s.polarity_scores(e['text'])['compound']
    query = "INSERT INTO tweets VALUES (%s, %s, %s);"
    pg.execute(query, (text, username, score))
