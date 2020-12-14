#%%

import zipfile
from matplotlib.pyplot import axis
import pandas as pd
from pandas.core.tools.datetimes import to_datetime
from pandas.io.parsers import read_csv
import numpy as np
#%%
#zf = zipfile.ZipFile('ECA_blended_custom.zip')
#file_ex = zf.extract('TG_STAID002759.txt')
#df = read_csv(file_ex, sep=" ", header=None, error_bad_lines=False)

df = read_csv('temp_data.txt', date_parser=True)

#%%
    """
01-06 SOUID: Source identifier
08-15 DATE : Date YYYYMMDD
17-21 TG   : mean temperature in 0.1 &#176;C
23-27 Q_TG : Quality code for TG (0='valid'; 1='suspect'; 9='missing')
    """

#%%
df.columns = ['id','date','temp','qc']
df.drop('id', axis = 1,inplace=True)
#%%
df['date'] = to_datetime(df['date'],format='%Y%m%d')
#%%
df.set_index('date',inplace=True)
#%%
#df[df['qc'] == 1] # I will ignore the cq 1 which doesn't seems different that the rest
df[df['qc'] == 9]
# %%
#Create na
df.loc[25316:25510,'temp'] = np.nan

# %%
df['temp'].interpolate(method='linear', inplace=True, extrapolate=True)

# %%
df['date'].dtype

# %%
