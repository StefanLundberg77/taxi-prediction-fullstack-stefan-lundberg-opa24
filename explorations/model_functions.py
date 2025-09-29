from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, make_scorer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd
import numpy as np
from taxipred.utils.constants import get_clean_data
from Cleaning_functions import split_features_target
from model_functions import train_evaluate

# # creating a dict for different estimators to evaluate
# models = {"linear": {"model": LinearRegression(), "scale": True},
#           "knn": {"model": KNeighborsRegressor(), "scale": True},
#           "svr": {"model": SVR(), "scale": True},
#           "rnd": {"model": RandomForestRegressor(), "scale": False},
#           "mlp": {"model": MLPRegressor(), "scale": True},
#           "ridge": {"model": Ridge(), "scale": True},
#           "lasso":{"model": Lasso(), "scale": True},
#           "xgb": {"model": XGBRegressor(), "scale": True}
# }

# method for tuning/validating different estimators
def train_evaluate(X_train, y_train, X_test, y_test, model): 
    
    

    # train & predict model
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    

    # evaluate
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # visualize results
    metrics = {
        "MAE": round(mae, 2),
        "MSE": round(mse, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 2)
    }
    # Export model
    # joblib.dump(model, model_path)
    #return model, metrics
    return model, metrics, 


def hyper_optimize(X_train, y_train, X_test, y_test, model): 
    
    models = model
    results = []
    best_model = None
    best_score = -float("inf")
    
    for name, model in models.items():
        steps = []
        if model["scale"]:
            steps.append(("scaler", StandardScaler()))
        steps.append(("model", model["model"]))
        
        # ensure y_train is 1D-array
        # if hasattr(y_train, "values") and y_train.ndim == 2:
        #     y_train = y_train.values.ravel()
    
        #get/set params
        pipeline = Pipeline(steps)
        grid = GridSearchCV(pipeline, pipeline.get_params(), cv=3, scoring="r2", n_jobs=-1)
        grid.fit(X_train, y_train)
    
        score = grid.best_score_
        results.append({
            "Model": name,
            "Best R2": score,
            "Best Params": grid.best_params_
        })

        if score > best_score:
            best_score = score
            best_model = grid.best_estimator_
            best_name = name
            
        pipeline.set_params(grid.best_params_)
    

    print(f"Best model: ({best_name})")