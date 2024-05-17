import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


import pickle
import pandas as pd

with open("model/model.pkl", "rb") as file:
    loaded_model = pickle.load(file)

# tt1179933,rl1329956353,10 Cloverfield Lane,PG-13,15000000.0,103.0,3427.0,24727437.0,72082999.0,7.2,355000.0,United States,Drama Horror Mystery Sci-Fi Thriller,358.0,88.32,0,3.0,2016.0

new_data = pd.DataFrame(
    {
        "month": [3],
        "year": [2016],
        "mpaa": ["PG-13"],
        "budget": [15000000],
        "runtime": [103],
        "screens": [3427],
        "opening_week": [24727437],
        "user_vote": [72082999],
        "ratings": [7.2],
        "critic_vote": [355000],
        "meta_score": [88.32],
        "country": ["United States"],
    }
)

label_encoder = LabelEncoder()
new_data["mpaa"] = label_encoder.fit_transform(new_data["mpaa"])
new_data["country"] = label_encoder.fit_transform(new_data["country"])

predicted_box_office = loaded_model.predict(new_data)
print(f"Predicted Domestic Box Office: {predicted_box_office[0]}")
