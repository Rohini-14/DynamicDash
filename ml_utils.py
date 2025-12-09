import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_models(df, target, features):
    X = df[features].copy()
    y = df[target].copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression(); lr.fit(X_train, y_train); lr_pred = lr.predict(X_test)
    rf = RandomForestRegressor(random_state=42, n_estimators=100); rf.fit(X_train, y_train); rf_pred = rf.predict(X_test)
    def metrics(y_true, y_pred):
        import math
        return {"MAE": float(mean_absolute_error(y_true, y_pred)),
                "RMSE": float(math.sqrt(mean_squared_error(y_true, y_pred))),
                "R2": float(r2_score(y_true, y_pred))}
    results = {"Linear Regression": metrics(y_test, lr_pred), "Random Forest": metrics(y_test, rf_pred)}
    importances = None
    try:
        importances = dict(zip(features, rf.feature_importances_.tolist()))
    except Exception:
        pass
    best_model = "Random Forest" if results["Random Forest"]["RMSE"] <= results["Linear Regression"]["RMSE"] else "Linear Regression"
    model_obj = rf if best_model == "Random Forest" else lr
    return {"results": results, "best_model_name": best_model, "best_model": model_obj, "importances": importances}
