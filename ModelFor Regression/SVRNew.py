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

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30 )


regressor = SVR(kernel='linear', C=1000, gamma= 0.0001).fit(X_train, Y_train)
print("Now printing the coeeficients:")
print(regressor.coef_)

X_train_encoded = StdS_X.inverse_transform(X_train)
Y_train_encoded = StdS_y.inverse_transform(Y_train)
print("The score in training data set is", regressor.score(X_train, Y_train))
print("The score in test data set is", regressor.score(X_test, Y_test))
y_hat = regressor.predict(X_test)
y_hat = np.array(y_hat)


y_hat_encoded = StdS_y.inverse_transform(y_hat.reshape(-1, 1))
y_hat_encoded = np.array(y_hat_encoded)
Y_test_encoded = StdS_y.inverse_transform(Y_test)
Y_test_encoded = np.array(Y_test_encoded)
predictions = pd.DataFrame({'y_test': Y_test_encoded.flatten(), 'y_hat': y_hat_encoded.flatten()})
print(predictions)
print("The r_sq is %.2f"%r2_score(Y_test_encoded, y_hat_encoded))
print("The mean absoulte error is %.2f"%mean_squared_error(Y_test_encoded, y_hat_encoded))
print("The mean square error is %.2f"%mean_absolute_error(Y_test_encoded, y_hat_encoded))
print("The explained variance score is %.2f"%explained_variance_score(Y_test_encoded, y_hat_encoded))

#sns.displot(Y_test-y_hat)
plt.scatter(Y_test_encoded, y_hat_encoded)
plt.xlabel("Actual or true value", fontsize = 14)
plt.ylabel("Predicted value", fontsize = 14)
plt.title("Actual vs predicted", fontsize = 14)
plt.savefig("C:\\Users\\Subiran\\Desktop\\My Dataset\\SVRLinearR2.jpg")
plt.show()




