import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D, Input
from keras.losses import MeanSquaredLogarithmicError
from keras.optimizers import Adam
fileName ='C:\\Users\\Subiran\\Desktop\\My Dataset\\AllImages.xlsx'

xl_file = pd.ExcelFile(fileName)
df_samples = pd.read_excel(fileName, engine='openpyxl')
X = df_samples.iloc[:, 1 : -1]
Y = df_samples.iloc[:, -1]
X = np.array(X).astype(float)
Y = np.array(Y).astype(float)
from sklearn.tree import DecisionTreeRegressor

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30)

regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(X_train, Y_train)

print("The score in training data set is", regressor.score(X_train, Y_train))
print("The score in test data set is", regressor.score(X_test, Y_test))
print("AFTER PARAMETER TUNING:::::")
print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

parameters={"splitter":["best","random"],
            "max_depth" : [1,3,5,7,9,11,12],
           "min_samples_leaf":[1,2,3,4,5,6,7,8,9,10],
           "min_weight_fraction_leaf":[0.1,0.2,0.3,0.4,0.5],
           "max_features":["log2","sqrt"],
           "max_leaf_nodes":[10,20,30,40,50,60,70,80,90] }

from sklearn.model_selection import GridSearchCV
tuning_model= GridSearchCV(regressor ,param_grid=parameters,scoring= 'r2', cv=3, verbose=3)

def timer(start_time=None):
    if not start_time:
        start_time=datetime.now()
        return start_time
    elif start_time:
        thour,temp_sec=divmod((datetime.now()-start_time).total_seconds(),3600)
        tmin,tsec=divmod(temp_sec,60)
        #print(thour,":",tmin,':',round(tsec,2))
from datetime import datetime

start_time=timer(None)

tuning_model.fit(X,Y)

timer(start_time)

print(tuning_model.best_params_)
print(tuning_model.best_score_)


