#%%
import matplotlib.pyplot as plt
import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense 
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.datasets import mnist
from keras import backend as K 
import tensorflow.keras

#%%
(X_train, y_train), (X_test, y_test) = mnist.load_data()

#%%
#*Make data 1D
X_train = X_train.reshape(60000,-1)
X_train.shape
pd.DataFrame(X_train)
#%%
#* Transform y into categories 
y_train = to_categorical(y_train)

#%%
#* Define the model - instantiate and object of the class Sequential
K.clear_session()
m = Sequential([
    Dense(units=100, activation='relu', input_shape=(1,784)), # hidden layer
    Dense(units=20, activation='relu'),
    Dense(units=20, activation='relu'),
    # with 2 neurons (units), activation='sigmoid', input_shape is only determined in the first layer  
    Dense(units=10, activation='softmax') # output layer
])

#%%
m.summary()

#%%
m.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
#Let's also try momentum

#%%
model_log = m.fit(X_train, y_train, batch_size=32, epochs=10, validation_split=0.2)

#%%

plt.plot(model_log.history['loss'], label='training_loss')
plt.plot(model_log.history['val_loss'], label='validation_loss')
plt.legend()

#%%
plt.plot(model_log.history['accuracy'])
plt.plot(model_log.history['val_accuracy'])

#%%

[round(prob, 6) for prob in m.predict(X_train[0:1])[0]]

#%%

