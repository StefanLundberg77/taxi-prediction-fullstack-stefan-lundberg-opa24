
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import time
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# method for crossvalidate, evaluate hyperparams and testresults
def cv_test_benchmark(X_train, y_train, X_test, y_test, df_models):
    results = []

    for row in df_models.itertuples(index=False):
        name  = row.name
        model = row.model
        scale = row.scale
        
        # list pipeline steps
        steps = []
        
        # scale data if suited for model
        if scale:
            steps.append(("scaler", StandardScaler()))
        steps.append(("model", model))
        pipeline = Pipeline(steps)

        # #get params
        parameters = generate_param_grid(name)
        
        #search.fit(X_train, y_train)
        grid = GridSearchCV(pipeline, parameters, cv=3, scoring="r2", n_jobs=-1)
        
        start = time.time()
        
        grid.fit(X_train, y_train)

        elapsed = time.time() - start
        
        # best model with params
        best_est = grid.best_estimator_

        # cross‑validation score
        cv_score = grid.best_score_

        # test score
        y_pred = best_est.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results.append({
            "model": name,
            "cv_R2": round(cv_score, 3), # gridsearch score
            "test_R2": round(r2, 3),
            "delta_cv_test": round(r2 - cv_score, 3), # diff
            "test_MAE": round(mae, 3),
            "test_MSE": round(mse, 3),
            "test_RMSE": round(rmse, 3),
            "train_time_sec": round(elapsed, 2),
            "best_params": grid.best_params_,
            "best_estimator": best_est
        })

    df_results = pd.DataFrame(results)
    return df_results

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




