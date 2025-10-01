
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd
import numpy as np

def hyper_optimize(X_train, y_train, df): 
    
    results = []
    best_score = -float("inf")   # <-- initiera här
    best_model = None
    best_name = None
    
    for row in df.itertuples(index=False):
        name  = row.name
        model = row.model
        scale = row.scale
        steps = []

        if scale:  # if model need scaling
            steps.append(("scaler", StandardScaler()))
        steps.append(("model", model))
          
        #get/set params
        parameters = generate_param_grid(name)
        pipeline = Pipeline(steps)

        #search.fit(X_train, y_train)
        grid = GridSearchCV(pipeline, parameters, cv=3, scoring="r2", n_jobs=-1)
        grid.fit(X_train, y_train)
    
        #score = search.best_score_
        score = grid.best_score_
        
        results.append({
            "model": name,
            "best r2": score,
            "best params": grid.best_params_
        })

        if score > best_score:
            best_score = score
            best_model = grid.best_estimator_
            best_name = name

        df = pd.DataFrame(results)
        
    return df, best_model, best_name

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
    return model, metrics 

def generate_param_grid(model):
    grids = {
        "linear": {"model__fit_intercept": [True, False]},
        "ridge": {"model__alpha": [0.1, 1.0, 10.0]},
        "lasso": {"model__alpha": [0.01, 0.1, 1.0]},
        "knn": {"model__n_neighbors": [3, 5, 7]},
        "svr": {"model__C": [0.1, 1, 10], "model__kernel": ["linear", "rbf"]},
        "mlp": {
            "model__hidden_layer_sizes": [(64,), (128,), (64, 32)],
            "model__activation": ["relu", "tanh"],
            "model__solver": ["adam", "lbfgs"],
            "model__learning_rate_init": list(np.linspace(0.001, 0.1, 5))
        },
        "xgb": {
            "model__n_estimators": [100, 200],
            "model__max_depth": [3, 5],
            "model__learning_rate": [0.05, 0.1]
        },
        "rf": {
            "model__n_estimators": [100, 200],
            "model__max_depth": [None, 10, 20]
        }
    }
    return grids.get(model, {})




