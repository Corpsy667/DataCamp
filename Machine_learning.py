import pandas as pd
import numpy as np
from Cleaning_data import importing_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

def predicting_data_and_fitting(data):
    X_train, X_test, y_train, y_test = train_test_split(data['Sentiment'], data['Popularity'])
    X_train = X_train.to_numpy().reshape(-1, 1)
    X_test = X_test.to_numpy().reshape(-1, 1)
    linearmodel = LogisticRegression()
    linearmodel.fit(X_train, y_train)
    y_pred = linearmodel.predict(X_test)

    mse=mean_squared_error(y_pred, y_test)
    print("Average cross-validation score:", mse)


def plotting_values(data):
    plt.scatter(data['Sentiment'], data['Popularity'])
    plt.show()

predicting_data_and_fitting(importing_data())