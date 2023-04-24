import cv2
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
from tqdm.notebook import tqdm
from PIL import Image
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D, Input, concatenate
from sklearn.model_selection import train_test_split
import tensorflow_hub as hub

BASE_DIR = 'C:/Users/Subiran/Desktop/Labeled dataset/ALLInOne'
image_paths = []
image_distance = []

for filename in tqdm(os.listdir(BASE_DIR)):
    image_path = os.path.join(BASE_DIR, filename)
    image_paths.append(image_path)

    pattern = image_path[image_path.rfind("_") + 1:len(image_path) - 4]
    image_distance.append(int(pattern))

df = pd.DataFrame()
df['image'], df['distance'] = image_paths, image_distance

def extract_features(images):
    features = []
    for image in tqdm(images):
        img = tf.keras.preprocessing.image.load_img(image)
        img = img.resize((224, 224), Image.ANTIALIAS)
        img = np.array(img)
        features.append(img)

    features = np.array(features)

    features = features.reshape(len(features), 224, 224, 3) # Width is 500 and height is 1000
    return features

X = extract_features(df['image']) # 53 numpy array of size 500*1000*3
X = X/255.0
Y = np.array(df['distance'])

IMAGE_SHAPE = (224, 224) + (3,)
base_model = tf.keras.applications.ResNet50V2(input_shape=IMAGE_SHAPE, include_top= False,  weights='imagenet')
base_model.trainable = True


features_train = base_model.predict(X)

print(X.shape) # 53 ota in the form of 53, 224, 224, 3

flat1 = Flatten()(base_model.layers[-2].output)
fc1 = Dense(64, activation='relu')(flat1)
output = Dense(1, activation='relu')(fc1)

model = Model(inputs = base_model.inputs, outputs = output)

print(model.summary())
model.compile(loss=['binary_crossentropy', 'mae'], optimizer='adam', metrics=['accuracy'])
#history = model.fit(x=X, y=Y, batch_size=16, epochs=30, validation_split=0.2, callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)])
history = model.fit(x=X, y=Y, batch_size=16, epochs=30, validation_split=0.2)

model.save('DistanceModelpretrained.h5')





