import numpy as np
import pandas as pd
pd.set_option('display.width', 700)
pd.set_option('display.max_columns', 10)
from pathlib import Path
import os.path
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import r2_score
from PIL import Image

import cv2

fileName = 'C:/Users/Subiran/Desktop/AgePredDataset/20-50/test/50/41251.jpg'
model = tf.keras.models.load_model('agemodel2/mymodel1dfhkje.h5')
model.summary()
"""""
new_image = tf.keras.preprocessing.image.load_img(fileName)
new_image = new_image.resize((128, 128))
new_image = np.array(new_image)

new_image = new_image / 255.0  # rescale the pixel values
new_image = new_image.reshape(1, 128, 128, 1)
# Predict the age of the new image
age_prediction = model.predict(new_image)
print('Predicted age withour opncv:', round(age_prediction[1][0][0]))
"""""


image = cv2.imread(fileName)
print(image.shape[:2])
image = cv2.resize(image, (128, 128))

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = image/255.0
image = image.reshape(1, 128, 128, 1)

age_prediction = model.predict(image)
#print('Predicted age:', round(age_prediction[1][0][0]))

print(age_prediction[0][0][0])
print(age_prediction[1][0][0])






