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

#print(Y)
# It helps to standarize the range of range of features and ensures that each feature(continuos variable) contributes equally to tha analysis.

Y =  Y.reshape(-1, 1)
StdS_X = StandardScaler() # rescales the data to have  a mean of 0 and a standard devaition of 1.
X = StdS_X.fit_transform(X) # In other words it subtracts each data with its means and divide it by the standard deviation
StdS_y = StandardScaler()
Y = StdS_y.fit_transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30, random_state= 30)
print(len(X_train))

hidden_units1 = 5
hidden_units2 = 5
hidden_units3 = 5
learning_rate = 0.01

def build_model_using_Sequential():
    model = Sequential([Dense(hidden_units1, kernel_initializer='normal', activation='relu'), Dropout(0.2),

                        #Dense(hidden_units2, kernel_initializer= 'normal', activation='relu'), Dropout(0.2),

                        Dense(hidden_units3, kernel_initializer= 'normal', activation='relu'),

                        Dense(1, kernel_initializer='normal', activation='relu')

                      ])
    return model

model = build_model_using_Sequential()


msle = MeanSquaredLogarithmicError()
model.compile(
    loss='mean_squared_logarithmic_error',
    optimizer=Adam(learning_rate=learning_rate),
    metrics=[msle]
)
history = model.fit(
    X_train,
    Y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[tf.keras.callbacks.EarlyStopping(monitor='mean_squared_logarithmic_error', patience=10, restore_best_weights=True)]
)

#print(Y_test)
y_hat = model.predict(X_test)
y_hat = np.array(y_hat) # But this is in encoded format:

y_hat_encoded = StdS_y.inverse_transform(y_hat.reshape(-1, 1))
y_hat_encoded = np.array(y_hat_encoded)
Y_test_encoded = StdS_y.inverse_transform(Y_test)
Y_test_encoded = np.array(Y_test_encoded)
predictions = pd.DataFrame({'y_test': Y_test_encoded.flatten(), 'y_hat': y_hat_encoded.flatten()})


print(predictions)

print("The r_sq is %.2f"%r2_score(Y_test_encoded, y_hat_encoded))
print("The mean Square error is %.2f"%mean_squared_error(Y_test_encoded, y_hat_encoded))
print("The mean Absolute error is %.2f"%mean_absolute_error(Y_test_encoded, y_hat_encoded))
print("The explained variance score is %.2f"%explained_variance_score(Y_test_encoded, y_hat_encoded))

#sns.displot(Y_test-y_hat)
plt.scatter(Y_test_encoded, y_hat_encoded)
plt.xlabel("Actual or true value", fontsize = 14)
plt.ylabel("Predicted value", fontsize = 14)
plt.title("Actual vs predicted", fontsize = 14)
#plt.savefig("C:\\Users\\Subiran\\Desktop\\My Dataset\\SVRLinearR2.jpg")
plt.show()


