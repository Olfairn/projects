"""
Read text corpus from HTML files,
vectorize and train a model
"""

import numpy as np
import os
import pickle
import re
from imblearn.over_sampling import SMOTE
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from bs4 import BeautifulSoup as soup


SONG_PATH = './songs/'


def read_songs():
    """extract all songs for all artists"""
    songs = []
    labels = []
    for artist in os.listdir(SONG_PATH):
        path = os.path.join(SONG_PATH, artist)
        print(f'\nreading songs by {artist}')
        for filename in tqdm(os.listdir(path)):
            if filename.endswith('.html'):
                html = open(os.path.join(path, filename)).read()  # returns one string
                songs.append(extract_lyrics(html))
                labels.append(artist)
    print(f'\nread {len(songs)} songs')
    return songs, labels


def extract_lyrics(html):
    """extract lyrics from html page"""
    song = soup(html, 'html.parser')
    section = song.find_all(attrs={'class':'lyric-body'})[0]
    lyrics = section.text
    lyrics = re.sub(r'[\n\-\?\.\,\(\)] | [\']', ' ', lyrics)  # clean
    return lyrics


def rebalance_dataset(X, y):
    """
    bootstrap all minority classes with less than 4 data points up to 6
    else SMOTE doesn't work
    """
    values, counts = np.unique(y, return_counts=True)
    small_classes = [x[0] for x in list(zip(values, counts)) if x[1] <=3]
    extra_x = [X]
    extra_y = [y]
    for c in small_classes:
        upsample_index = np.where(y==c)[0]
        extra_x.append(X[upsample_index])
        extra_y.append(y[upsample_index])

    extra_x = tuple([x.todense() for x in extra_x])
    X = np.concatenate(extra_x, axis=0)
    y = np.concatenate(extra_y, axis=0)
    sm = SMOTE(sampling_strategy='auto')
    X, y = sm.fit_resample(X, y)
    return X,y


def train_model(X, y):
    """update the Naive Bayes model"""
    pipeline = make_pipeline(
        TfidfVectorizer(),  #TODO: improve tokenization
        #TODO: add rebalance_dataset here
        MultinomialNB(alpha=0.5) #TODO: hyperparameter search
    )
    pipeline.fit(X, y)

    # initial evaluation
    print(f"\ntraining accuracy: {pipeline.score(X, y):6.3f}")
    cv = cross_val_score(pipeline, X, y, cv=5)
    print(f"\ncross-val accuracies: {cv.round(3)}")

    return pipeline


if __name__ == "__main__":
    corpus, labels = read_songs()  #TODO: make this a separate step -> faster
    print(corpus, labels)
    Xtrain, Xtest, ytrain, ytest = train_test_split(corpus, labels, random_state=23)
    m = train_model(Xtrain, ytrain)

    # estimate of the model error
    # uncomment when you are done optimizing
    print(f"test_score: {m.score(Xtest, ytest):6.3f}")

    # fit model on entire data before saving
    m.fit(corpus, labels)
    pickle.dump(m, open('lyrics_model.pickle', 'wb'))
