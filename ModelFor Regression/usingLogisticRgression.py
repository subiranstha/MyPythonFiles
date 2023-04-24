import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
from sklearn.linear_model import LogisticRegression

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

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30 )

regressor = LogisticRegression()
regressor.fit(X_train, Y_train)

