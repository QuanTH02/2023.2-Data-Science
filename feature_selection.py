import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from scipy.stats import pearsonr
from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    cross_val_score,
)
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from factor_analyzer import FactorAnalyzer
import pickle

df = pd.read_csv("merged_data/final_merged.csv")

unique_genres = set(genre for sublist in df["genres"].str.split() for genre in sublist)
for genre in unique_genres:
    df[genre] = df["genres"].apply(lambda x: 1 if genre in x.split() else 0)
df = df.drop(columns=["genres"])

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
] + list(unique_genres)
df = df[selected_columns]

genre_columns = list(unique_genres)
genre_data = df[genre_columns]
scaler = StandardScaler()
genre_data_scaled = scaler.fit_transform(genre_data)

fa = FactorAnalyzer()
fa.fit(genre_data_scaled)
eigenvalues, _ = fa.get_eigenvalues()
n_factors = sum(eigenvalues > 1)
print(f"Number of factors to retain: {n_factors}")

fa = FactorAnalyzer(n_factors=n_factors, rotation="varimax")
fa.fit(genre_data_scaled)
factor_scores = fa.transform(genre_data_scaled)

factor_scores_df = pd.DataFrame(
    factor_scores, columns=[f"Factor{i+1}" for i in range(n_factors)]
)

df = pd.concat([df, factor_scores_df], axis=1)

df = df.drop(columns=genre_columns)

mpaa_label_encoder = LabelEncoder()
country_label_encoder = LabelEncoder()
df["mpaa"] = mpaa_label_encoder.fit_transform(df["mpaa"])
df["country"] = country_label_encoder.fit_transform(df["country"])

X = df.drop("domestic_box_office", axis=1)
y = df["domestic_box_office"]
y_log = np.log(y)


# Feature selection based on correlation with target
correlation_threshold = 0.2
selected_features = [
    column
    for column in X.columns
    if abs(pearsonr(X[column], y_log)[0]) > correlation_threshold
]

# Keep only selected features
X = X[selected_features]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

# Preprocessing pipeline for numerical features
numeric_features = selected_features
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
    ]
)


def randomized_search(model, param_distributions):
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", model),
        ]
    )
    search = RandomizedSearchCV(
        pipeline,
        param_distributions,
        n_iter=50,
        cv=5,
        n_jobs=-1,
        scoring="neg_mean_squared_error",
        random_state=42,
    )
    search.fit(X_train, y_train)
    return search


param_grid_rf = {
    "regressor__n_estimators": [50, 100, 150],
    "regressor__max_depth": [None, 10, 20, 30],
    "regressor__min_samples_split": [2, 5, 10],
}

param_grid_gb = {
    "regressor__n_estimators": [50, 100, 150],
    "regressor__max_depth": [3, 5, 7],
    "regressor__learning_rate": [0.01, 0.1, 0.2],
}

param_grid_xgb = {
    "regressor__n_estimators": [50, 100, 150],
    "regressor__max_depth": [3, 5, 7],
    "regressor__learning_rate": [0.01, 0.1, 0.2],
    "regressor__subsample": [0.8, 0.9, 1.0],
}

param_grid_lgbm = {
    "regressor__n_estimators": [50, 100, 150],
    "regressor__max_depth": [-1, 10, 20],
    "regressor__learning_rate": [0.01, 0.1, 0.2],
    "regressor__num_leaves": [31, 50, 100],
}

param_grid_cb = {
    "regressor__iterations": [50, 100, 150],
    "regressor__depth": [4, 6, 10],
    "regressor__learning_rate": [0.01, 0.1, 0.2],
    "regressor__l2_leaf_reg": [1, 3, 5],
}

models = [
    (RandomForestRegressor(random_state=42), param_grid_rf),
    (GradientBoostingRegressor(random_state=42), param_grid_gb),
    (XGBRegressor(random_state=42), param_grid_xgb),
    (LGBMRegressor(random_state=42), param_grid_lgbm),
    (CatBoostRegressor(random_state=42, verbose=0), param_grid_cb),
]

best_score = float("inf")
best_model = None
best_params = None

for model, param_grid in models:
    search = randomized_search(model, param_grid)
    if -search.best_score_ < best_score:
        best_score = -search.best_score_
        best_model = search.best_estimator_
        best_params = search.best_params_

print(f"Best model: {best_model}")
print(f"Best parameters: {best_params}")
print(f"Best score: {best_score}")

y_pred_log = best_model.predict(X_test)
y_pred = np.expm1(y_pred_log)
y_test_actual = np.expm1(y_test)

mse = mean_squared_error(y_test_actual, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test_actual, y_pred)
r2 = r2_score(y_test_actual, y_pred)
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R^2 Score: {r2}")

scores = cross_val_score(best_model, X, y_log, cv=5, scoring="neg_mean_squared_error")
rmse_scores = np.sqrt(-scores)
print(f"Cross-validated RMSE scores: {rmse_scores}")
print(f"Mean RMSE: {rmse_scores.mean()}")
print(f"Standard deviation of RMSE: {rmse_scores.std()}")

# Save the model and preprocessors
with open("model_efa/best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
with open("model_efa/mpaa_label_encoder.pkl", "wb") as f:
    pickle.dump(mpaa_label_encoder, f)
with open("model_efa/country_label_encoder.pkl", "wb") as f:
    pickle.dump(country_label_encoder, f)
with open("model_efa/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("model_efa/factor_analyzer.pkl", "wb") as f:
    pickle.dump(fa, f)
with open("model_efa/unique_genres.pkl", "wb") as f:
    pickle.dump(unique_genres, f)
with open("model_efa/selected_features.pkl", "wb") as f:
    pickle.dump(selected_features, f)
