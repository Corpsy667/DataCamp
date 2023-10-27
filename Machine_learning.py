from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def predicting_data_and_fitting(data):
    X_train, X_test, y_train, y_test = train_test_split(data[data['Popularity'] != 0]['Sentiment'], data[data['Popularity'] != 0]['Popularity'], random_state=2)
    scaler = StandardScaler()
    X_train_standardized = scaler.fit_transform(X_train.to_numpy().reshape(-1, 1))
    X_test_standardized = scaler.transform(X_test.to_numpy().reshape(-1, 1))
    gradient_boosting = GradientBoostingRegressor(n_estimators=100,
                                                  random_state=0)  # You can adjust n_estimators and other hyperparameters as needed
    gradient_boosting.fit(X_train_standardized, y_train)
    """y_pred = gradient_boosting.predict(X_test_standardized)
    print(y_pred, y_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("RMSE score:", rmse)

    R2 = r2_score(y_test, y_pred)
    print("R2 Score is :", R2)"""
    #KNN also had a great value but it looked more like a regressor problem
    return gradient_boosting



def plotting_values(data):
    plt.scatter(data['Sentiment'], data['Popularity'])
    plt.xlabel('Sentiments')
    plt.ylabel('Popularity')
    plt.show()

#predicting_data_and_fitting(importing_data())
