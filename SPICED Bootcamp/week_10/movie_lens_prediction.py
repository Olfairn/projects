#%%
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import KNNImputer
from sklearn.decomposition import NMF

plt.rcParams['figure.figsize'] = (12,6)
#%%
#links = pd.read_csv('data/links.csv') #not usefull 
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv("data/ratings.csv")

#%%
movies.columns[1]
#tags = pd.read_csv('data/tags.csv') # ignore for now
#%%
ratings.drop(columns='timestamp',inplace=True)
df = ratings.merge(movies[['movieId','title']])

#%%
df.drop(columns='movieId',inplace=True)

#%%
#? How many users, movies and rating
df['userId'].unique().shape
df['movieId'].unique().shape
df['rating'].shape

#? Average amount of rating per movie
df[['userId','title']].groupby('title').size().plot(kind='hist')
#%%
#? Average amount of rating per user
df[['userId','rating']].groupby('userId').count().plot(kind='hist')
df[['userId','rating']].groupby('userId').count().median()

#%%
#*Pivot
df_table = df.pivot_table(index='userId',columns='title',values='rating')

#%%
#Impute with KNNI
imputer = KNNImputer()
df_imputed = pd.DataFrame(imputer.fit_transform(df_table),index=df_table.index,columns=df_table.columns)
#%%
#!------- NMF (Non-Negative Matrix Factorization)  ------
#* Build model 

# Instantiate the nmf
nmf = NMF(n_components=30, max_iter=200) # n_components: # of features
nmf.fit(df_imputed)

# Extract the movie-feature matrix
Q = nmf.components_

# Extract the user-feature matrix
P = nmf.transform(df_imputed)

#pd.DataFrame(P, index=df_imputed.index)
round(nmf.reconstruction_err_, 2)

#Reconstruct Original matrix
R_hat = pd.DataFrame(np.matmul(P, Q), index=df_imputed.index, columns=df_imputed.columns)
R_hat

#%%
#* Make pred

# Create a dictionary for a new user
new_user_input = {"'71 (2014)": 5, 'Zulu (2013)': 4} # similar to JSON data that we will have to work with in the end

# Convert it to a pd.DataFrame
new_user = pd.DataFrame(new_user_input, columns=df_imputed.columns, index=['Stefan'])

#Fill missing data
average_movie_rating = df_table.mean().mean()
new_user = new_user.fillna(average_movie_rating)

#Prediction step 1 - generate user_P 
user_P = nmf.transform(new_user)

#new user R - reconstruct R but for this new user only
user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=df_table.columns)

# Get rid of movies we have already watchend
recommendation = user_R.drop(columns=new_user_input.keys())

# Sort recommendations
recommendation.sort_values(by='Stefan', axis=1, ascending=False)


#!------- Fuzzy Match ------

#%%
import jellyfish as jf

#%%

movies_ = df['title']
movie_input = ['12 angry','Shreck']

def get_closest_match(x, list_random):
    best_match = None
    highest_jaro_wink = 0
    for current_string in list_random:
        current_score = jf.jaro_winkler(x, current_string)
        if(current_score > highest_jaro_wink):
            highest_jaro_wink = current_score
            best_match = current_string
    return best_match

for movie_inputs in movie_input:
    result = get_closest_match(movie_inputs,movies_)
    print (f'The movie input was {movie_inputs}, and the guess is  {result}')
    

#%%

#!------- Cosine Similarity  ------


def cosim(vec1, vec2):
    """function to calcualte the cosine similarity between two vectors"""
    
    num = np.dot(vec1, vec2)
    denom = np.sqrt(np.dot(vec1, vec1)) * np.sqrt(np.dot(vec2, vec2))
    return num / denom

# Create some user vectors and check the similarity
ronny = R_imputed.loc['Ronny'].iloc[0]
mustafa = R_imputed.loc['Mustafa']

cosim(ronny, mustafa)


#%%
#! Save model

import pickle
with open('model.pickle','wb') as file:
    pickle.dump(nmf,file)
    
#%%
with open('df.csv','wb') as file:
    pickle.dump(df_imputed,file)

#%%
df_imputed
#%%
#Open model

with open('model.pickle','rb') as file:
    model = pickle.load(nmf,file)
    

#%%

def compute_nmf(model, dataset,user_input):
    Q = model.components_
    P = model.transform(dataset)
    new_user = pd.DataFrame(user_input, columns=dataset.columns, index=['user1'])
    average_movie_rating = dataset.mean().mean()
    new_user = new_user.fillna(average_movie_rating)
    user_P = model.transform(new_user)
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=dataset.columns)
    recommendation = user_R.drop(columns=user_input.keys())
    recommendation = recommendation.sort_values(by='user1', axis=1, ascending=False)
    return recommendation


test_data = {"'71 (2014)": 5}

df2 = compute_nmf(nmf,df_imputed,test_data)
# %%
def compute_nmf(model, dataset,user_input):
    Q = model.components_
    P = model.transform(dataset)
    new_user = pd.DataFrame(user_input, columns=dataset.columns, index=['user1'])
    average_movie_rating = dataset.mean().mean()
    new_user = new_user.fillna(average_movie_rating)
    user_P = model.transform(new_user)
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=dataset.columns)
    recommendation = user_R.drop(columns=user_input.keys())
    recommendation = recommendation.sort_values(by='user1', axis=1, ascending=False)
    recommendation = recommendation.to_dict()
    return recommendation


test_data = {"'71 (2014)": 5}

df2 = compute_nmf(nmf,df_imputed,test_data)
#%%
list(df2.keys())[0:10]

