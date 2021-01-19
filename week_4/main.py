#%%

import pandas as pd
import copy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer 
import nltk
import os
import re

#%%
#nirvana = pd.read_csv('data/Nirvana.csv')
#jimi = pd.read_csv('data/Jimi_Hendrix.csv')
#doors = pd.read_csv('data/The_Doors.csv')
beatles = pd.read_csv('data/beatles.csv',dtype=str, keep_default_na=False)
stones = pd.read_csv('data/stones.csv',dtype=str,)
#%%
#nirvana['artist'] = 'Nirvana'
#jimi['artist'] = 'Jimi Hendrix'
#doors['artist'] = 'The Dorrs'
beatles['artist'] = 'The Beatles'
stones['artist'] = 'The Rolling Stones'

#nirvana.rename(columns = {'Nirvana':'lyrics'}, inplace=True)
#jimi.rename(columns = {'Jimi Hendrix':'lyrics'}, inplace=True)
#doors.rename(columns = {'The doors':'lyrics'}, inplace=True)

df = pd.concat([stones,beatles],ignore_index=True)
df.dropna()

#%%

df['lyrics'] = df['lyrics'].str.replace('[^\w\s]','')
df['lyrics'] = df['lyrics'].str.replace('\\n',' ')
df['lyrics'] = df['lyrics'].str.lower()

#%%
df.dropna(inplace=True)

#%%
df = df[df['lyrics'].notna()]
df['lyrics'] = df['lyrics'].astype(str)

#%%    
# #Text Lemmatization

#nltk.download('wordnet')
#nltk.download('punkt')

lemmatizer = WordNetLemmatizer() 
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()

def lemmatize_text(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

df["lyrics_lema"] = df['lyrics'].apply(lemmatize_text)

#%%
# Identifying Stop Words
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def stop_word(text):
    return [x for x in text if x not in ENGLISH_STOP_WORDS]

#%%
#Delete stop words
df["lyrics_stop_lema"] = df["lyrics_lema"].apply(lambda a: [word for word in a if word not in ENGLISH_STOP_WORDS])
df
#%%

df["lyrics_stop_lema_function"] = df["lyrics_lema"].apply(stop_word)

#%%
df

#%%
#Turn it back to string
df["lyrics_stop_lema"] = df["lyrics_stop_lema"].apply(lambda x: ' '.join(map(str, x)))

#Let's do that later

#let's try imbalanced learn ?
#%%

X = df['lyrics_stop_lema']
y = df['artist']
#%%
# Train, test split

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    stratify = y, 
                                                    random_state = 42)

#%%
from train_model import train_model
m = train_model(X_train,y_train)

#%%
#Manage class imbalance
df['artist'].value_counts() #the amount of song is quite balanced
df['word_count'] = df['lyrics_stop_lema'].str.split().str.len()
df[['artist','word_count']].groupby('artist').sum() #But the about of words isn't
#%%
from imblearn.over_sampling import RandomOverSampler, SMOTE
from train_model import rebalance_dataset

rebalance_dataset(X,y) #doesn't work because df
#%%
print(f"test_score: {m.score(X_test, y_test):6.3f}")

#%%
# fit model on entire data before saving
m.fit(X, y)
prediction = m.predict_proba(['sympathie for the devil'])

print('\n This looks like a song from:')
artists = m.steps[-1][1].classes_   
print(artists[prediction.argmax()])
print(f'probability: {prediction.max():.3f}')

# %%
