#%%
import pickle
import pandas as pd
import numpy as np

# Import model
with open('nmf_model.pickle','rb') as file:
    nmf = pickle.load(file)


#%%
# Import data
with open('df.csv','rb') as file:
    df = pickle.load(file)

#df = pd.read_csv('df.csv')
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
    recommendation = recommendation.to_dict()
    return recommendation

#%%

def get_movie_recommendation(dict_name_rating):
    print(dict_name_rating)
    return compute_nmf(nmf,df,dict_name_rating)



