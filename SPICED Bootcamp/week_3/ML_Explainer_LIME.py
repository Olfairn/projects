
#Local Interpretable Model-agnostic Explanations (LIME)

#%%
# from https://pythondata.com/local-interpretable-model-agnostic-explanations-lime-python/
from sklearn.datasets import load_boston
import sklearn.ensemble
import numpy as np
from sklearn.model_selection import train_test_split
import lime
import lime.lime_tabular

#%%
boston = load_boston()

rf = sklearn.ensemble.RandomForestRegressor(n_estimators=30, max_depth= 8,
              min_samples_split= 4)
train, test, labels_train, labels_test = train_test_split(boston.data, boston.target, train_size=0.80)
rf.fit(train, labels_train)

#%%
print('Random Forest MSError', np.mean((rf.predict(test) - labels_test) ** 2))

#%%
print('MSError when predicting the mean', np.mean((labels_train.mean() - labels_test) ** 2))

# Extract a single tree: 
import matplotlib.pyplot as plt
from sklearn import tree

fn=boston.feature_names
cn=['price']
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=800)
tree.plot_tree(rf.estimators_[0],
               feature_names = fn, 
               class_names=cn,
               filled = True)
fig.savefig('rf_individualtree.png')
#%%
boston.target_names
#%%
categorical_features = np.argwhere(
    np.array([len(set(boston.data[:,x]))
    for x in range(boston.data.shape[1])]) <= 10).flatten()

print(categorical_features)

#%%
np.array([len(set(boston.data[:,x]))
#%%
explainer = lime.lime_tabular.LimeTabularExplainer(train, 
                                                   feature_names=boston.feature_names, 
                                                   class_names=['price'], 
                                                   categorical_features=categorical_features, 
                                                   verbose=True, mode='regression')

#%%
i = 101

exp = explainer.explain_instance(test[i], rf.predict, num_features=5)
exp.show_in_notebook(show_table=True)
# %%
