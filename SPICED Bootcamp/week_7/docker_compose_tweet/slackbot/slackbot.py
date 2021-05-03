import requests
import time
import config
from sqlalchemy import create_engine

#time.sleep(10) 

pg = create_engine('postgres://postgres:postgres@postgres:5432/postgres', echo=True)

webhook_url = config.webhook_url

query = ('''
    SELECT username, text, score FROM tweets ORDER BY score desc LIMIT 1
;
''')

while True:

    tweets = pg.execute(query)
    tweet_list = list(tweets)[0]
    
    # Before
    requests.post(url = webhook_url, json = {"text": f"\n--- Berlin ---\nUser {tweet_list[0]} wrote:"})
    
    # Text
    requests.post(url = webhook_url, json = {"text": tweet_list[1]})
    
    # After
    requests.post(url = webhook_url, json = {"text": f"The sentiment score is {tweet_list[2]}.\n------------\n"})
    
    time.sleep(100)