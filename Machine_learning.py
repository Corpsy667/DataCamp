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

def predicting_data_and_fitting(data):
    X_train, X_test, y_train, y_test = train_test_split(data['Sentiment'], data['Popularity'])
    X_train = X_train.to_numpy().reshape(-1, 1)
    X_test = X_test.to_numpy().reshape(-1, 1)
    linearmodel = KNeighborsClassifier()
    linearmodel.fit(X_train, y_train)
    y_pred = linearmodel.predict(X_test)

    # Create a KNN classifier
    knn = KNeighborsClassifier(n_neighbors=5)  # You can set the number of neighbors (k) here

    # Perform k-fold cross-validation
    cv_scores = cross_val_score(knn, X_train, y_train, cv=5)  # Replace X and y with your data

    # Print the cross-validation scores
    print("Cross-validation scores:", cv_scores)

    # Calculate and print the average cross-validation score
    avg_cv_score = cv_scores.mean()
    print("Average cross-validation score:", avg_cv_score)


def plotting_values(data):
    plt.scatter(data['Sentiment'], data['Popularity'])
    plt.show()

predicting_data_and_fitting(importing_data())