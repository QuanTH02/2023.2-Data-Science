import pandas as pd
import numpy as np
import pickle

# tt1389072,rl628917761,Downsizing,R,68000000.0,135.0,2668.0,4954287.0,24449754.0,5.8,125000.0,United States,Drama Fantasy Sci-Fi,349.0,49.34,0,12.0,2017.0
# tt0240462,rl1112442369,Dr. Dolittle 2,PG,72000000.0,87.0,3053.0,25037039.0,112952899.0,4.7,47000.0,United States,Comedy Family Fantasy,135.0,42.66,0,6.0,2001.0
# tt0219653,rl1515095553,Dracula 2000,R,54000000.0,100.0,2204.0,8636567.0,33022767.0,4.9,37000.0,"Canada, United States",Action Fantasy Horror Thriller,14.0,26.0,0,12.0,2000.0
# tt0829150,rl1531872769,Dracula Untold,PG-13,70000000.0,92.0,2900.0,23514615.0,56280355.0,6.2,208000.0,United States,Action Drama Fantasy Horror,168.0,27.68,0,10.0,2014.0
# tt2223990,rl1598981633,Draft Day,PG-13,25000000.0,110.0,2781.0,9783603.0,28842237.0,6.8,67000.0,United States,Drama Sport,196.0,58.99,0,4.0,2014.0
# tt1127180,rl1380877825,Drag Me to Hell,PG-13,30000000.0,99.0,2510.0,15825480.0,42100625.0,6.6,218000.0,United States,Horror,302.0,91.05,0,5.0,2009.0
# tt0372873,rl1263437313,Dragon Wars: D-War,PG-13,32000000.0,107.0,2277.0,5376000.0,10977721.0,3.5,25000.0,"Republic of Korea, United States",Action Drama Fantasy Thriller,47.0,29.77,0,9.0,2007.0
# tt1098327,rl1447986689,Dragonball Evolution,PG,30000000.0,85.0,2181.0,4756488.0,9362785.0,2.5,79000.0,United States,Action Adventure Fantasy Sci-Fi Thriller,10.0,45.0,0,4.0,2009.0
# tt0259288,rl1464763905,Dragonfly,PG-13,60000000.0,104.0,2507.0,10216025.0,30323400.0,6.1,40000.0,"Germany, United States",Drama Fantasy Mystery Romance Thriller,158.0,10.76,0,2.0,2002.0
# tt1462041,rl3192817153,Dream House,PG-13,50000000.0,92.0,2664.0,8129355.0,21302340.0,6.0,69000.0,"Canada, United States",Drama Mystery Thriller,106.0,11.23,0,9.0,2011.0
# tt0285531,rl3092153857,Dreamcatcher,R,68000000.0,136.0,2945.0,15027423.0,33715436.0,5.5,97000.0,"Canada, United States",Drama Horror Sci-Fi Thriller,219.0,29.21,0,3.0,2003.0
# tt0418647,rl3142485505,Dreamer,PG,32000000.0,106.0,2735.0,9178233.0,32751093.0,6.8,14000.0,United States,Drama Family Sport,28.0,59.0,0,10.0,2005.0
# tt0443489,rl3176039937,Dreamgirls,PG-13,75000000.0,130.0,2797.0,378950.0,103365956.0,6.6,77000.0,United States,Drama Musical,245.0,78.55,0,12.0,2006.0
# tt1343727,rl2823718401,Dredd,R,50000000.0,98.0,2557.0,6278491.0,13414714.0,7.1,295000.0,"India, South Africa, United Kingdom, United States",Action Crime Sci-Fi,200.0,77.0,0,9.0,2012.0
# tt0817538,rl2924381697,Drillbit Taylor,PG-13,40000000.0,110.0,3061.0,10309986.0,32862104.0,5.7,62000.0,United States,Action Comedy Crime,178.0,29.44,0,3.0,2008.0
# tt0780504,rl2706277889,Drive,R,15000000.0,100.0,2904.0,11340461.0,35061555.0,7.8,706000.0,United States,Action Drama,320.0,91.12,0,9.0,2011.0

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
    prediction = np.expm1(prediction_log)  
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
    "sequel" : 0.0,
    "genres": "Horror Mystery Thriller",
}

predicted_revenue = predict_revenue(new_movie)
#predicted_revenue = predict_with_feature_selection(new_movie)
print("Predicted revenue:", predicted_revenue)
