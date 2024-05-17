import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd



# tt1179933,rl1329956353,10 Cloverfield Lane,PG-13,15000000.0,103.0,3427.0,24727437.0,72082999.0,7.2,355000.0,United States,Drama Horror Mystery Sci-Fi Thriller,358.0,88.32,0,3.0,2016.0

def predict_opening_week(month, year, mpaa, budget, runtime, screens, opening_week, user_vote, ratings, critic_vote, meta_score, country):
    with open("model/best_model.pkl", "rb") as file:
        loaded_model = pickle.load(file)

    new_data = pd.DataFrame(
        {
            "month": [month],
            "year": [year],
            "mpaa": [mpaa],
            "budget": [budget],
            "runtime": [runtime],
            "screens": [screens],
            "opening_week": [opening_week],
            "user_vote": [user_vote],
            "ratings": [ratings],
            "critic_vote": [critic_vote],
            "meta_score": [meta_score],
            "country": [country],
        }
    )

    label_encoder = LabelEncoder()
    new_data["mpaa"] = label_encoder.fit_transform(new_data["mpaa"])
    new_data["country"] = label_encoder.fit_transform(new_data["country"])

    predicted_box_office = loaded_model.predict(new_data)
    print(f"Predicted Domestic Box Office: {np.expm1(predicted_box_office[0])}")
    return np.expm1(predicted_box_office[0])

def predict_no_opening_week(month, year, mpaa, budget, runtime, screens, critic_vote, meta_score, country):
    with open("model/best_model_no_opening_week.pkl", "rb") as file:
        loaded_model = pickle.load(file)
        
    new_data = pd.DataFrame(
        {
            "month": [month],
            "year": [year],
            "mpaa": [mpaa],
            "budget": [budget],
            "runtime": [runtime],
            "screens": [screens],
            "critic_vote": [critic_vote],
            "meta_score": [meta_score],
            "country": [country],
        }
    )

    label_encoder = LabelEncoder()
    new_data["mpaa"] = label_encoder.fit_transform(new_data["mpaa"])
    new_data["country"] = label_encoder.fit_transform(new_data["country"])

    predicted_box_office = loaded_model.predict(new_data)
    print(f"Predicted Domestic Box Office: {np.expm1(predicted_box_office[0])}")
    return np.expm1(predicted_box_office[0])

if __name__ == '__main__':
    predict_opening_week(3, 2016, "PG-13", 15000000, 103, 3427, 24727437, 72082999, 7.2, 355000, 88.32, "United States")