
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import pandas as pd
import numpy as np

def hyper_optimize(X_train, y_train,  model): 
    
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
        parameters = generate_param_grid(name)
        pipeline = Pipeline(steps)
        #search = RandomizedSearchCV(
        #     pipeline,
        #     param_distributions=parameters,
        #     n_iter=10000, # set correct
        #     cv=3,
        #     scoring="r2",
        #     random_state=42,
        #     n_jobs=-1
        # )
        #search.fit(X_train, y_train)
        grid = GridSearchCV(pipeline, parameters, cv=3, scoring="r2", n_jobs=-1)
        grid.fit(X_train, y_train)
    
        #random_score = search.best_score_
        grid_score = grid.best_score_
        
        results.append({
            "Model": name,
            "Best R2": grid_score,
            "Best Params": grid.best_params_
        })

        if grid_score > best_score:
            best_score = grid_score
            best_model = grid.best_estimator_
            best_name = name

        df_results = pd.DataFrame(results)
        
    return df_results

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

def tune_model(results_df, model_name, model): #wtf

    row = results_df[results_df["Model"] == model_name]
    if row.empty:
        raise ValueError(f"Modell '{model_name}' not fount")
    
    best_params = row.iloc[0]["Best Params"]
    if not isinstance(best_params, dict):
        raise ValueError("Not a dictionary.")
    
    clean_params = {k.replace("model__", ""): v for k, v in best_params.items()}
    
    original_model = model[model_name]["model"]
    
    original_params = original_model.get_params()
    
    combined_params = {**original_params, **clean_params}
    
    return model(**combined_params)


