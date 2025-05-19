from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

target_variable = ["interested"]


def train_model_ridge(dataframe):
    model_object = {}
    print("Training Ridge Regression")
    print(dataframe.columns.tolist())
    ridge = linear_model.Ridge(alpha=0.5)
    X_train, X_test, y_train, y_test = train_test_split(dataframe.drop(target_variable, axis=1),
                                                        dataframe.charges)
    model = ridge.fit(X_train, y_train)
    model.fit(X_train, y_train)
    model_object["model"] = model
    model_object["training_features"] = X_train.columns.tolist()
    return model_object


def train_model_with_grid_search(dataframe):
    print("Training Ridge Regression")
    print(dataframe.columns)
    ridge = linear_model.Ridge()
    params_grid = {
        "alpha": [0.01, 0.05, 0.1, 0.5]
    }
    X_train, X_test, y_train, y_test = train_test_split(dataframe.drop(target_variable, axis=1),
                                                        dataframe.Sales)
    model = GridSearchCV(ridge, param_grid=params_grid, verbose=2, cv=5, refit=True, n_jobs=5)
    model.fit(X_train, y_train)
    return model.best_estimator_


def train_random_forest(dataframe):
    X_train, X_test, y_train, y_test = train_test_split(dataframe.drop(target_variable, axis=1),
                                                        dataframe.interested)
    print("Training Random Forest")
    rf = RandomForestClassifier(n_estimators=100, n_jobs=5,verbose=2)
    rf.fit(X_train, y_train)
    return rf


def test_model(dataframe,model):
    df = dataframe.drop(target_variable, axis=1)
    print("Accuracy of the model is : ",accuracy_score(model.predict(df),dataframe['interested']))
    #return model.predict(df)



if __name__ == '__main__':
    pass
