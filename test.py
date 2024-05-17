import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


label_encoder = LabelEncoder()


movie = {
    "month": 5.0,
    "year": 2017.0,
    "mpaa": "PG-13",
    "budget": 5300000.0,
    "runtime": 89.0,
    "screens": 2270.0,
    "opening_week": 11205562.0,
    "country": "United States",
    "user_vote": 5.6,
    "ratings": 61000.0,
    "critic_vote": 103.0,
    "meta_score": 5.0,
}
# Chuyển đổi thuộc tính mpaa và country sang dạng số
movie["mpaa"] = label_encoder.fit_transform([movie["mpaa"]])[0]
movie["country"] = label_encoder.fit_transform([movie["country"]])[0]

# Tạo một DataFrame từ dictionary movie
movie_df = pd.DataFrame([movie])

# Tiền xử lý dữ liệu của phim cần dự đoán
numeric_features = [
    "month",
    "year",
    "budget",
    "runtime",
    "screens",
    "opening_week",
    "user_vote",
    "critic_vote",
    "meta_score",
    "ratings",
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
        ("regressor", RandomForestRegressor(n_estimators=150, random_state=42)),
    ]
)

with open("model/model.pkl", "rb") as file:
    pipeline = pickle.load(file)

# Dự đoán doanh thu của phim
revenue_predict = pipeline.predict(movie_df)

print("Predicted revenue:", revenue_predict)
# Đánh giá mô hình