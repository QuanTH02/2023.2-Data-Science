import pandas as pd
import numpy as np
import pickle


def predict_revenue(movie):
    with open("model_efa/best_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model_efa/mpaa_label_encoder.pkl", "rb") as f:
        mpaa_label_encoder = pickle.load(f)
    with open("model_efa/country_label_encoder.pkl", "rb") as f:
        country_label_encoder = pickle.load(f)
    with open("model_efa/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("model_efa/factor_analyzer.pkl", "rb") as f:
        fa = pickle.load(f)
    with open("model_efa/unique_genres.pkl", "rb") as f:
        unique_genres = pickle.load(f)

    movie["mpaa"] = mpaa_label_encoder.transform([movie["mpaa"]])[0]
    movie["country"] = country_label_encoder.transform([movie["country"]])[0]

    new_movie_genres = np.array(
        [
            1 if genre in movie.get("genres", "").split() else 0
            for genre in unique_genres
        ]
    ).reshape(1, -1)
    new_movie_genres_scaled = scaler.transform(new_movie_genres)
    new_movie_factors = fa.transform(new_movie_genres_scaled)

    movie.update(
        {
            f"Factor{i+1}": new_movie_factors[0, i]
            for i in range(new_movie_factors.shape[1])
        }
    )

    movie_df = pd.DataFrame([movie])

    predicted_revenue_log = model.predict(movie_df)
    predicted_revenue = np.expm1(predicted_revenue_log)
    return predicted_revenue

def predict_with_feature_selection(movie):
    with open("model_efa/best_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model_efa/mpaa_label_encoder.pkl", "rb") as f:
        mpaa_label_encoder = pickle.load(f)
    with open("model_efa/country_label_encoder.pkl", "rb") as f:
        country_label_encoder = pickle.load(f)
    with open("model_efa/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("model_efa/factor_analyzer.pkl", "rb") as f:
        fa = pickle.load(f)
    with open("model_efa/unique_genres.pkl", "rb") as f:
        unique_genres = pickle.load(f)
    with open("model_efa/selected_features.pkl", "rb") as f:
        selected_features = pickle.load(f)

    movie["mpaa"] = mpaa_label_encoder.transform([movie["mpaa"]])[0]
    movie["country"] = country_label_encoder.transform([movie["country"]])[0]

    new_movie_genres = np.array(
        [
            1 if genre in movie.get("genres", "").split() else 0
            for genre in unique_genres
        ]
    ).reshape(1, -1)
    new_movie_genres_scaled = scaler.transform(new_movie_genres)
    new_movie_factors = fa.transform(new_movie_genres_scaled)

    movie.update(
        {
            f"Factor{i+1}": new_movie_factors[0, i]
            for i in range(new_movie_factors.shape[1])
        }
    )

    movie_df = pd.DataFrame([movie])
    movie_df = movie_df[selected_features]
    prediction_log = model.predict(movie_df)
    prediction = np.expm1(prediction_log)  # Inverse the log transformation
    return prediction[0]

new_movie = {
    "month": 5.0,
    "year": 2017.0,
    "mpaa": "PG-13",
    "budget": 5300000.0,
    "runtime": 89.0,
    "screens": 2270.0,
    "opening_week": 11205562.0,
    "country": "United States",
    "user_vote": 61000.0,
    "ratings": 5.6,
    "critic_vote": 103.0,
    "meta_score": 50.0,
    "genres": "Horror Mystery Thriller",
}

predicted_revenue = predict_revenue(new_movie)
#predicted_revenue = predict_with_feature_selection(new_movie)
print("Predicted revenue:", predicted_revenue)
