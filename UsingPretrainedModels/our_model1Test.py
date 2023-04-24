import numpy as np
import pandas as pd
pd.set_option('display.width', 700)
pd.set_option('display.max_columns', 10)
from pathlib import Path
import os.path
from sklearn.model_selection import train_test_split
import tensorflow as tf


import cv2

fileName = 'C:/Users/Subiran/Desktop/Labeled dataset/147 Mircometer/LM2301-0595_566.jpg'
model = tf.keras.models.load_model('DistanceModelpretrained.h5')
model.summary()

new_image = tf.keras.preprocessing.image.load_img(fileName)
new_image = new_image.resize((224, 224))
new_image = np.array(new_image)

new_image = new_image / 255.0  # rescale the pixel values
new_image = new_image.reshape(1, 224, 224, 3)
# Predict the age of the new image
age_prediction = model.predict(new_image)
print('Predicted age withour opncv:', (age_prediction[0][0]))

#print(age_prediction)
