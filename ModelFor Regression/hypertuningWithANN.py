import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D, Input
from sklearn.metrics import make_scorer, accuracy_score
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV

fileName ='C:\\Users\\Subiran\\Desktop\\My Dataset\\AllImages.xlsx'

xl_file = pd.ExcelFile(fileName)
df_samples = pd.read_excel(fileName, engine='openpyxl')
X = df_samples.iloc[:, 1 : -1]
Y = df_samples.iloc[:, -1]
X = np.array(X).astype(float)
Y = np.array(Y).astype(float)

#print(Y)
# It helps to standarize the range of range of features and ensures that each feature(continuos variable) contributes equally to tha analysis.

Y =  Y.reshape(-1, 1)
StdS_X = StandardScaler() # rescales the data to have  a mean of 0 and a standard devaition of 1.
X = StdS_X.fit_transform(X) # In other words it subtracts each data with its means and divide it by the standard deviation
StdS_y = StandardScaler()
Y = StdS_y.fit_transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30)

def make_regression_ann(fl, sl, initializer='uniform', activation='relu', optimizer='adam', loss='mse'):

    model = Sequential()
    model.add(Dense(units=fl, kernel_initializer=initializer, activation=activation))
    model.add(Dense(units=sl, kernel_initializer=initializer, activation=activation))
    model.add(Dense(1, kernel_initializer=initializer))
    model.compile(loss=loss, optimizer=optimizer)

    return model

def build_fn(fl, sl):
    return make_regression_ann(fl = fl, sl = sl)

first_layer = [5, 10, 15, 20, 30]
second_layer = [5, 10, 15, 20, 30]
best_para = []
for i in first_layer:
    for j in second_layer:
        param_grid = {
            'initializer': ['normal', 'uniform'],
            'activation': ['relu'],
            'optimizer': ['adam', 'rmsprop'],
            'loss': ['mse', 'mae'],
            'batch_size': [32, 64],
            'epochs': [5, 10, 20, 30, 40, 50, 100],
        }

        grid_search =  GridSearchCV(estimator= KerasRegressor(build_fn = make_regression_ann, fl = i, sl = j, verbose=3), param_grid=param_grid,
                                   scoring='neg_mean_absolute_percentage_error',cv=3)
        grid_search.fit(X, Y, verbose=3)
        print("For the First Layer=", i, " and second layer =", j, "The best parameters are")
        best_para.append(grid_search.best_params_)
        print(grid_search.best_params_)

print(best_para)
