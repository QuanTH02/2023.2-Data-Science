import pickle
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

data = pd.read_csv("merged_data/final_merged.csv")

selected_columns = [
    "month",
    "year",
    "mpaa",
    "budget",
    "runtime",
    "screens",
    "opening_week",
    "domestic_box_office",
    "user_vote",
    "ratings",
    "critic_vote",
    "meta_score",
    "country",
]
data = data[selected_columns]
data.dropna(inplace=True)

label_encoder = LabelEncoder()
data["mpaa"] = label_encoder.fit_transform(data["mpaa"])
data["country"] = label_encoder.fit_transform(data["country"])

X = data.drop("domestic_box_office", axis=1)
y = data["domestic_box_office"]

y_log = np.log1p(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

numeric_features = [
    "month",
    "year",
    "budget",
    "runtime",
    "screens",
    "opening_week",
    "user_vote",
    "ratings",
    "critic_vote",
    "meta_score",
]
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(random_state=42)),
    ]
)

param_grid = {
    "regressor__n_estimators": [50, 100, 150],
    "regressor__max_depth": [None, 10, 20, 30],
    "regressor__min_samples_split": [2, 5, 10],
}

grid_search = GridSearchCV(
    pipeline, param_grid, cv=5, n_jobs=-1, scoring="neg_mean_squared_error"
)
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_}")

best_model = grid_search.best_estimator_
y_pred_log = best_model.predict(X_test)

y_pred = np.expm1(y_pred_log)
y_test_actual = np.expm1(y_test)

mse = mean_squared_error(y_test_actual, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_actual, y_pred)
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R^2 Score: {r2}")

scores = cross_val_score(best_model, X, y, cv=5, scoring="neg_mean_squared_error")
rmse_scores = np.sqrt(-scores)

print(f"Cross-validated RMSE scores: {rmse_scores}")
print(f"Mean RMSE: {rmse_scores.mean()}")
print(f"Standard deviation of RMSE: {rmse_scores.std()}")

with open("model/best_model.pkl", "wb") as file:
    pickle.dump(best_model, file)
