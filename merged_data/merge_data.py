import pandas as pd
# Đọc dữ liệu từ file CSV
df_a = pd.read_csv("../mojo/data/all_movie_mojo.csv")
df_b = pd.read_csv("../the-numbers/data/all_the-numbers.csv")

# Thêm cột genres cho df_b với giá trị ""
df_b["genres"] = ""
df_b.drop("international_box_office", axis=1, inplace=True)
df_b.drop("worldwide_box_office", axis=1, inplace=True)
print(df_a.info())
print(df_b.info())
# Gộp dữ liệu từ hai DataFrame
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
        "month",
        "year"
    ],
    how="outer",
    suffixes=("_a", "_b"),
)

print(merged_df.info())

# Tạo hàm để lấy giá trị lớn hơn
def choose_greater_value(value_a, value_b):
    if pd.isna(value_a):
        return value_b
    elif pd.isna(value_b):
        return value_a
    else:
        return max(value_a, value_b)


# Áp dụng hàm cho các cột cần so sánh
cols_to_compare = ["mpaa"]
for col in cols_to_compare:
    merged_df[col] = merged_df.apply(
        lambda row: (
            row[f"{col}_a"] if not pd.isna(row[f"{col}_a"]) else row[f"{col}_b"]
        ),
        axis=1,
    )

# Lấy giá trị lớn hơn cho các cột còn lại
cols_to_get_greater = [
    "budget",
    "runtime",
    "screens",
    "opening_week",
    "domestic_box_office",
]
for col in cols_to_get_greater:
    merged_df[col] = merged_df.apply(
        lambda row: choose_greater_value(row[f"{col}_a"], row[f"{col}_b"]), axis=1
    )

merged_df["genres"] = merged_df["genres_a"]

print(merged_df.info())

# Loại bỏ các cột dư thừa
columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)

# Lưu kết quả vào file mới
print(merged_df.info())
merged_df.to_csv("merged.csv", index=False)

merged_df.dropna(
    subset=[
        "month",
        "year",
        "runtime",
        "budget",
        "mpaa",
        "screens",
        "opening_week",
        "domestic_box_office",
    ],
    inplace=True,
)
print(merged_df.info())
merged_df.to_csv("filtered_merged_data.csv", index=False)

print("Tổng hợp dữ liệu thành công và lưu vào file 'merged.csv'.")
