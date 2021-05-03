#%%
pip install requests
pip insta

#%%

import re
import requests
import time
import pandas as pd
import pickle
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#%%
song_urls = []
lyrics = []
    
 # Fetch HTML code for artist's overview page
code = requests.get(artist_url, headers = headers)

artist_songs = {} # Use a dict to filter out double songs (no double key is possible)

soup = BeautifulSoup(code.text)
            
# Find the URLs for this artist's songs
for a in soup.find_all("a"):
# Exclude "none" types
    if type(a.get("href")) is str: 
                    # Filter: only lyrics links
    if a.get("href").startswith("/lyric"):
    # Create a dict entry for a particular song with its URL (only add link if song is not yet existent)
    artist_songs.setdefault(a.text, "https://www.lyrics.com/" + a.get("href"))
            
            # Add each song URL of this artist to song_urls
            for url in artist_songs.values():
                song_urls.append([artist, url])            

        except KeyError:
            print(f"Error: Artist {artist} not found!")
            

    # Loop through the found song URLs of all artists
    for i, song in enumerate(song_urls):
        print(f"fetching song {i+1} from {len(song_urls)}...")
        # Get HTML source code for song
        source = requests.get(song[1], headers = headers)
        soup = BeautifulSoup(source.text)
        lyric = soup.find(id = "lyric-body-text").text
        # Append lyric text to list
        lyrics.append([song[0], lyric])
        time.sleep(1)
        
    return(lyrics)




def clean_text(texts, lemmatize = True, stopwords = True):
    """
    Clean the lyric texts
    """
    import copy
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

    output = copy.deepcopy(texts) 
        
    for i, text in enumerate(output):
        
        print(f"Cleaning lyric {i+1} of {len(output)}")
        
        text[1] = re.sub("-", "", text[1]) # remove hyphens
        
        if lemmatize:
            import en_core_web_sm # from spacy
            en = en_core_web_sm.load()        
            text[1] = " ".join([word.lemma_ for word in en(text[1])])
                
        text[1] = text[1].lower()
        text[1] = re.sub("\d", "", text[1]) # remove numbers
        text[1] = re.sub("\W", " ", text[1]) # Remove non-text characters
        text[1] = re.sub("\s+[a-z]\s+", " ", text[1]) # Remove single characters
        text[1] = re.sub("^[a-z]\s+", "", text[1]) # Remove single characters at the beginning
        text[1] = re.sub("\s[a-z]$", "", text[1]) # Remove single characters at the end
        text[1] = re.sub("\s+", " ", text[1])
        
        if stopwords:
            text[1] = " ".join([word for word in text[1].split(" ") if word not in ENGLISH_STOP_WORDS])
            
        text[1] = re.sub("^\s", "", text[1]) # Remove spaces at the beginning
        text[1] = re.sub("\s$", "", text[1]) # Remove spaces at the end

    return(output)



def run_model(estimator, X_train, y_train):
    
    estimator.fit(X_train, y_train)
    
    y_pred = estimator.predict(X_train)
    
    from sklearn.metrics import classification_report
    
    print(classification_report(y_train, y_pred))
    
    return(estimator, y_pred)



def tune_model(estimator, X_train, y_train, param_grid, scoring, cv = 5):
    
    from sklearn.model_selection import GridSearchCV

    gridsearch = GridSearchCV(estimator = estimator, 
                              scoring = scoring,
                              param_grid = param_grid, 
                              cv = cv,
                              verbose = False)

    gridsearch.fit(X_train, y_train)
    
    print("CV results (mean test score):")
    print(gridsearch.cv_results_["mean_test_score"])

    print("Best score:")
    print(gridsearch.best_score_)
    
    print("Best parameters:")
    print(gridsearch.best_params_)
    
    return gridsearch
