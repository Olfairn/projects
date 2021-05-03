#%%
import numpy as np
import matplotlib.pyplot as plt
#%%

with np.load('simplified-recipes-1M.npz', allow_pickle=True) as data:
    recipes = data['recipes']
    ingredients = data['ingredients']

#%%
#Flatten and count Ingredients
flat_rep = np.hstack(recipes)
unique, counts = np.unique(flat_rep, return_counts=True)
ing_count = np.array(counts)
#%%
ing_count = np.array(counts)
ingredients

#%%
#Zip count with ingredient name
name_ing_count = dict(zip(ingredients,ing_count))

#%%
#The ingredients follow a log curve
plt.bar(name_ing_count.keys(), name_ing_count.values(),log=True)
plt.show()

#%%
plt.hist(ing_count,log=True)
plt.show()
#%%

#? How many ingredients? 

#? Distribution ingredients? --> should we exclude some? 

plt.plot(ingredients)
plt.show()

#%%
recipes[0]
#%%


for ing in recipes:
    if (ing == 800).any():
        print(recipes.key)
#TODO Clean non ingredients names like "bottle"

# %%
np.where(ingredients =='salt')
ingredients[recipes[0]]
ing_count[ingredients[1]]


#%%
import numpy as np

#%%
test_array = np.array([1.48,1.41,0.0,0.1])
#%%
arrange_test = test_array.argsort()
print(arrange_test)

#%%
test_array
