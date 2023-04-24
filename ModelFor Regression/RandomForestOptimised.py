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

regressor = RandomForestRegressor(bootstrap= False, max_depth= 10, max_features= 'log2', min_samples_leaf= 2,
                                  min_samples_split= 2, n_estimators= 2000, random_state=0)
regressor.fit(X_train, Y_train)
print("The score in training data set is", regressor.score(X_train, Y_train))
print("The score in test data set is", regressor.score(X_test, Y_test))
y_hat = regressor.predict(X_test)
y_hat = np.array(y_hat)
predictions = pd.DataFrame({'y_test': Y_test.flatten(), 'y_hat': y_hat})
print(predictions)
print("The r_sq is %.2f"%r2_score(Y_test, y_hat))
print("The mean absoulte error is %.2f"%mean_squared_error(Y_test, y_hat))
print("The mean square error is %.2f"%mean_absolute_error(Y_test, y_hat))
print("The explained variance score is %.2f"%explained_variance_score(Y_test, y_hat))

#sns.displot(Y_test-y_hat)
plt.scatter(Y_test, y_hat)
plt.xlabel("Actual or true value", fontsize = 14)
plt.ylabel("Predicted value", fontsize = 14)
plt.title("Actual vs predicted", fontsize = 14)
plt.savefig("C:\\Users\\Subiran\\Desktop\\My Dataset\\RandomForestRSquare.jpg")
plt.show()




