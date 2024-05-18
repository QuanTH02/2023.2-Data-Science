import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from factor_analyzer import FactorAnalyzer
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("mpaa_label_encoder.pkl", "rb") as f:
    mpaa_label_encoder = pickle.load(f)
with open("country_label_encoder.pkl", "rb") as f:
    country_label_encoder = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("factor_analyzer.pkl", "rb") as f:
    fa = pickle.load(f)
with open("unique_genres.pkl", "rb") as f:
    unique_genres = pickle.load(f)

new_data = pd.read_csv("path_to_new_data.csv")

for genre in unique_genres:
    new_data[genre] = new_data["genres"].apply(lambda x: 1 if genre in x.split() else 0)
new_data = new_data.drop(columns=["genres"])

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
new_data = new_data[selected_columns]

new_genre_data = new_data[list(unique_genres)]
new_genre_data_scaled = scaler.transform(new_genre_data)

new_factor_scores = fa.transform(new_genre_data_scaled)
new_factor_scores_df = pd.DataFrame(
    new_factor_scores,
    columns=[f"Factor{i+1}" for i in range(new_factor_scores.shape[1])],
)

new_data = pd.concat([new_data, new_factor_scores_df], axis=1)
new_data = new_data.drop(columns=list(unique_genres))

new_data["mpaa"] = mpaa_label_encoder.transform(new_data["mpaa"])
new_data["country"] = country_label_encoder.transform(new_data["country"])

X_new = new_data.drop("domestic_box_office", axis=1)
y_new = new_data["domestic_box_office"]
y_new_log = np.log(y_new)

old_data = pd.read_csv("merged_data/preprocess_data.csv")
X = old_data.drop("domestic_box_office", axis=1)
y = old_data["domestic_box_office"]
y_log = np.log(y)

X = pd.concat([X, X_new], axis=0)
y_log = pd.concat([pd.Series(y_log), pd.Series(y_new_log)], axis=0)

update_data = pd.concat([X, y_log], axis=1)
update_data.to_csv("merged_data/preprocess_data.csv", index=False)

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
] + [f"Factor{i+1}" for i in range(new_factor_scores.shape[1])]
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", model.named_steps["regressor"]),
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
    search.fit(X, y_log)
    return search


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

with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
with open("mpaa_label_encoder.pkl", "wb") as f:
    pickle.dump(mpaa_label_encoder, f)
with open("country_label_encoder.pkl", "wb") as f:
    pickle.dump(country_label_encoder, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("factor_analyzer.pkl", "wb") as f:
    pickle.dump(fa, f)
with open("unique_genres.pkl", "wb") as f:
    pickle.dump(unique_genres, f)
