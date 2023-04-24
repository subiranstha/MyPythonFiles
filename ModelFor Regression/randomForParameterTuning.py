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

# Here feature scaling is not required as they are invariant to that:

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30)
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(random_state=0)
regressor.fit(X_train, Y_train)

n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['log2', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4, 5, 6, 8, 10]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

from sklearn.model_selection import GridSearchCV
tuning_model = GridSearchCV(regressor ,param_grid= random_grid,scoring= 'neg_mean_squared_error', cv=3, verbose=3)

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
