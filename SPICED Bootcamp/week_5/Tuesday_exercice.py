#%%
import pandas as pd
import seaborn as sns

#%%
df = pd.read_csv('flights_remainder.csv')
#%%
df['lag1'] = df['remainder'].shift(1)

#%%
df.corr()
sns.scatterplot(x='lag1',y='remainder',data=df)

#%%
df['lag2'] = df['remainder'].shift(2)
df['lag3'] = df['remainder'].shift(3)
df['lag4'] = df['remainder'].shift(4)
df['lag5'] = df['remainder'].shift(5)
df['lag6'] = df['remainder'].shift(6)
df['lag7'] = df['remainder'].shift(7)
df['lag8'] = df['remainder'].shift(8)
df['lag9'] = df['remainder'].shift(9)



df.corr()

# %%
#sns.scatterplot(x='lag1',y='remainder',data=df, alpha=0.5)
#sns.scatterplot(x='lag2',y='remainder',data=df, alpha=0.5)
sns.scatterplot(x='lag3',y='remainder',data=df, alpha=0.9)