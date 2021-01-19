#%%

import zipfile
import matplotlib as mpl
import pandas as pd
from pandas.core.reshape.reshape import get_dummies
from pandas.core.tools.datetimes import to_datetime
from pandas.io.parsers import read_csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from statsmodels.tsa.ar_model import AutoReg
import seaborn as sns
import plotly.express as px

mpl.rcParams['figure.figsize'] = (12,10)

#%%
df = read_csv('temp_data.txt', date_parser=True)
#%%
df.columns = ['id','date','temp','qc']
df.drop('id', axis = 1,inplace=True)
#%%
df['date'] = to_datetime(df['date'],format='%Y%m%d')
#%%
df.set_index('date',inplace=True)
#%%
df[df['qc'] == 1] # I will ignore the cq 1 which doesn't seems different that the rest
df[df['qc'] == 9]
# %%
#Filling in missing data step

#Create na
#df.loc[25316:25510,'temp'] = np.nan

#%%
df_small = df.loc['1946-01-01'::]
#%%
df_small['temp'] = df_small['temp'] /10
df_small.drop('qc',axis = 1, inplace=True)
#%%
df_small.plot()

#%%
df_small['rolling_temp'] = df_small.iloc[:,0].rolling(window=365).mean()
print(df_small['rolling_temp'].plot())
df_small.drop('rolling_temp', axis=1,inplace=True)

#%%
#Create a time_step
df_small['time_step'] = range(len(df_small))

#%%
#Dummifiy months
month_dummies = pd.get_dummies(df_small.index.month, prefix='month', drop_first=True).set_index(df_small.index)
df_small = df_small.join(month_dummies)
#%%
#Train / test split
df_small_train = df_small.iloc[:-365]
X_train = df_small.drop('temp',axis=1).iloc[:-365]
y_train = df_small[['temp']].iloc[:-365]
X_test= df_small.drop('temp',axis=1).iloc[-365:]
y_test = df_small[['temp']].iloc[-365:]
#%%
m = LinearRegression()
m.fit(X_train, y_train)

#%%
df_small_train['trend_month'] = m.predict(X_train)

#%%
#Plot the trend_month vs. temp
df_small_train[['temp','trend_month']].plot()

#%%
#Extract remainder:
df_small_train['remainder'] = df_small_train['temp'] - df_small_train['trend_month']

#%%
df_small_train['remainder'].plot()

#%%
#use Statsmodel to model it
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
selected_order = ar_select_order(df_small_train['remainder'], maxlag=10)
selected_order.ar_lags

#%%
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
print(plot_pacf(df_small_train['remainder']));
print(plot_acf(df_small_train['remainder']));

#%%

df_small_train['lag1'] = df_small_train['remainder'].shift(1)
df_small_train['lag2'] = df_small_train['remainder'].shift(2)
df_small_train['lag3'] = df_small_train['remainder'].shift(3)
df_small_train.dropna(inplace=True)

#%%
df_small_train
#%%
y_train_full = df_small_train['temp']
X_train_full = df_small_train.drop(columns=['remainder','temp','trend_month'])

#%%
m_full = LinearRegression()
m_full.fit(X_train_full,y_train_full)

#%%
df_small_train['predition_full_model'] = m_full.predict(X_train_full)

#%%
sns.lineplot(data=df_small_train[['temp','predition_full_model']])
#df_small_train.plot(df_small_train[['temp','predition_full_model']])

#%%
#Let's evaluate the model
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
ts_split = TimeSeriesSplit(n_splits=5)

time_series_split = ts_split.split(X_train_full, y_train_full) 

result = cross_val_score(estimator=m_full, X=X_train_full, y=y_train_full, cv=time_series_split)
result

#%%
#Let's test out model

X_test['trend_month'] = m.predict(X_test)

#%%
#Let's do some ARIMA
from statsmodels.tsa.arima.model import ARIMA
#df.drop('qc',axis=1,inplace=True)
df = df[df['temp'] > -100]

#%%
df.drop('qc',axis=1,inplace=True)
#%%
arima_model = ARIMA(df, order=(2,0,2)).fit()
#%%
arima_model.summary()

#%%


#%%
plt.plot(arima_model.predict(), label='arima')

#%%
plt.plot(arima_model.predict(), label='arima')

#%%
plot_pacf(df);
#%%
fig = px.line(df)
fig.update_xaxes(
    rangeslider_visible=True
)
fig.show()
#%%
from pmdarima import auto_arima

model = auto_arima(df_small2,
                    m = 12, seasonal=True,
                    start_p=0, start_q=0, max_order=4, test='adf', suppress_warning=True, stepwise=True,trace=True)

#%%
    """[ m = The period for seasonal differencing, m refers to the number of periods in each season. 
    For example, m is 4 for quarterly data, 12 for monthly data, or 1 for annual (non-seasonal) data.]
    """


#%%
model.summary()

#%%
model.fit(df_small['temp'])
#%%
X_a_train = df_small[['temp']].iloc[:-365]
X_a_test = df_small[['temp']].iloc[-365:]

X_a_train
history = [x for x in X_a_train]
predictions = list()
#%%
for t in range(len(X_a_test)):
	model = ARIMA(history, order=(2,0,2))
	model_fit = model.fit()
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = X_a_test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))

#%%
# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()

# ?
# ! 
# TODO 
#%%
from fbprophet import Prophet

#%%
Pro_train = df_small[['temp']].iloc[:-365].reset_index()
Pro_test = df_small[['temp']].iloc[-365:].reset_index()

Pro_train.columns = ['ds','y']
Pro_test.columns = ['ds','y']

#%%
m_pro = Prophet(weekly_seasonality = True)
m_pro.fit(Pro_train)

#%%
future = m_pro.make_future_dataframe(periods=21150)
future.tail()

#%%
forecast = m_pro.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

#%%
fig1 = m_pro.plot(forecast)

#%%
fig2 = m_pro.plot_components(forecast)

#%%
from fbprophet.plot import plot_plotly, plot_components_plotly

plot_plotly(m_pro, forecast)

#%%
plot_components_plotly(m_pro, forecast)
