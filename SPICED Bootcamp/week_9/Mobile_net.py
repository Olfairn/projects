#%%
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input

im = image.load_img('tram.jpg', target_size=(224, 224))
a = image.img_to_array(im)
a = a.reshape(1, 224, 224, 3)
a = preprocess_input(a)

from tensorflow.keras.applications import MobileNet

m = MobileNet(input_shape=(224, 224, 3)
m.compile(optimizer='rmsprop', loss='categorical_crossentropy',
           metrics=['accuracy'])