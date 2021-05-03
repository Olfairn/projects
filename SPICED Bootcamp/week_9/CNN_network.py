#%%
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense 
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten
from keras import backend as K 
import tensorflow.keras
from tensorflow.keras.applications import MobileNet



#%%
(X_train, y_train), (X_test, y_test) = mnist.load_data()

#%%
#*Add one D 
X_train = X_train.reshape(60000,28,28,1)
X_train.shape
#%%
#* Transform y into categories 
y_train = to_categorical(y_train)


#%%
m = Sequential([
    Conv2D(30, kernel_size=(3, 3), strides=(2, 2),
           padding="same", activation="relu",
           input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"),
    
    Flatten(),
    Dense(units=90, activation='relu'),
    Dense(units=10, activation='softmax') # output layer
])

    
#%%
m.summary()

#%%
m.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
#Let's also try momentum

#%%
model_log = m.fit(X_train, y_train, batch_size=80, epochs=15, validation_split=0.15)

#%%

plt.plot(model_log.history['loss'], label='training_loss')
plt.plot(model_log.history['val_loss'], label='validation_loss')
plt.legend()

#%%
plt.plot(model_log.history['accuracy'])
plt.plot(model_log.history['val_accuracy'])

#%%
X_test = X_test.reshape(10000,28,28,1)


#%%
m_predict = m.predict_classes(X_test)

compare = y_test == m_predict
test_validity =  np.count_nonzero(compare) / 10000
test_validity


#%%
df = pd.DataFrame(compare)

#%%
df.columns = ['prediction']
#%%
index_false = df[df['prediction']==False].index

small_index = [6,158,359,445,448]

x = np.arange(0,10)
y = np.arange(0,10)

#%%
for i in range(100): # shows first 100 images (X-datapoints)
    plt.subplot(10, 10, i+1)
    plt.imshow(X_train[i], cmap=plt.cm.Greys)
    plt.axis('off')
