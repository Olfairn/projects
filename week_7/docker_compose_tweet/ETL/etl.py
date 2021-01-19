import pymongo
import time
from sqlalchemy import create_engine

time.sleep(10) 

client = pymongo.MongoClient("mongodb")
db = client.tweets

entries = db.collections.tweets.find(limit=5)
for e in entries:
    print(e)

pg = create_engine('postgres://postgres:postgres@postgres:5432/postgres', echo=True)

