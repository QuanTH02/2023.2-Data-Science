import pandas as pd

df = pd.read_csv("imdb_merged.csv")

df["min_revenue"] = df["domestic_box_office"] * 0.9
df["max_revenue"] = df["domestic_box_office"] * 1.1

df.to_csv("test_data.csv", index=False)