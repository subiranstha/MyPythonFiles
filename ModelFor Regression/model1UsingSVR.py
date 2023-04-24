import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from joblib import dump
from sklearn.model_selection import train_test_split

fileName ='C:\\Users\\Subiran\\Desktop\\My Dataset\\AllImages.xlsx'

xl_file = pd.ExcelFile(fileName)

df_samples = pd.read_excel(fileName, engine='openpyxl')

X = df_samples.iloc[:, 1 : -1]
Y = df_samples.iloc[:, -1]

print(type(X))  # It is a panda data frame object:

print(X.shape)
print(Y.shape)
X = np.array(X)
Y = np.array(Y)

Y =  Y.reshape(-1, 1)
StdS_X = StandardScaler()
X = StdS_X.fit_transform(X)
StdS_y = StandardScaler()
Y = StdS_y.fit_transform(Y)
# Splitting the data in training and testing

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state= 30 )

print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)


# We directly go to Support vector regressor:

regressor = SVR(kernel='rbf').fit(X_train, Y_train)
 # Printing the R square of the model:

# Predicting the value of a new data:
"""""
arr1 = np.array([[3950, 4, 0]])
print(arr1.shape)
arr1 = StdS_X.transform(arr1)

value = regressor.predict(arr1)
value = np.array(value)
value = value.reshape(-1, 1)
value = StdS_y.inverse_transform(value)
print("Value is", value)
"""""
# Just finding out different accuracies:
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
"""""
ytrain_pred = regressor.predict(X_train)

print("The r_sq is %.2f"%r2_score(Y_train, ytrain_pred))
print("The mean absoulte error is %.2f"%mean_squared_error(Y_train, ytrain_pred))
print("The mean square error is %.2f"%mean_absolute_error(Y_train, ytrain_pred))
print("The explained variance score is %.2f"%explained_variance_score(Y_train, ytrain_pred))
"""""
# Predicting on the testing data:

print("Now testing on the test data")
ytest_pred = regressor.predict(X_test)
print("The r_sq is %.2f"%r2_score(Y_test, ytest_pred))
print("The mean absoulte error is %.2f"%mean_squared_error(Y_test, ytest_pred))
print("The mean square error is %.2f"%mean_absolute_error(Y_test, ytest_pred))
print("The explained variance score is %.2f"%explained_variance_score(Y_test, ytest_pred))







