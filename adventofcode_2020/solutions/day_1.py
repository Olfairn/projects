#%%
import pandas as pd 

df = pd.read_csv('input.txt', delimiter="\t", header=None)

for x in range(200):
    for y in range(200):
        for z in range(200):
            if (df[0][x] + df[0][y] + df[0][z]) == 2020:
                print(df[0][x] * df[0][y] * df[0][z])
    
    

