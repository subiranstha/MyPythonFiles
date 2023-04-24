import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score

fileName ='C:\\Users\\Subiran\\Desktop\\My Dataset\\AllImages.xlsx'

xl_file = pd.ExcelFile(fileName)

df_samples = pd.read_excel(fileName, engine='openpyxl')

X = df_samples.iloc[:, 1 : -1]
Y = df_samples.iloc[:, -1]

X = np.array(X)
Y = np.array(Y)

Y =  Y.reshape(-1, 1)
StdS_X = StandardScaler()
X = StdS_X.fit_transform(X)
StdS_y = StandardScaler()
Y = StdS_y.fit_transform(Y)
# Splitting the data in training and testing

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state= 30 )


regressor = SVR(kernel='linear').fit(X_train, Y_train)
k = 5

parameters = [{'kernel': ['linear'], 'gamma': [1e-4, 1e-3, 0.01, 0.1, 0.2, 0.5, 0.6, 0.9],'C': [1, 10, 50, 100, 300, 500, 1000]}]

from sklearn.model_selection import GridSearchCV
tuning_model = GridSearchCV(regressor ,param_grid= parameters ,scoring= 'r2', cv=k, verbose=3)

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




