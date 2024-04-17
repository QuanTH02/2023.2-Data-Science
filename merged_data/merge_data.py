import pandas as pd
'''
# Đọc file CSV và xử lý lỗi
try:
    df = pd.read_csv("all_movie_mojo.csv")
except pd.errors.ParserError as e:
    print(f"Có lỗi khi đọc file CSV: {e}")
    with open("all_movie_mojo.csv", "r", errors="replace") as file:
        lines = file.readlines()

    # Tạo DataFrame từ các dòng gây ra lỗi
    error_lines = [
        line for line in lines if len(line.split(",")) > 13
    ]  # Giả sử có 13 trường
    not_error_lines = [
        line for line in lines if len(line.split(",")) <= 13
    ]
    fix_error_lines = []
    for error_line in error_lines:
        error_line_split = error_line.split(",")
        print(error_line_split[7])

        if error_line_split[7] == 'None':
            error_line_split[7] = error_line_split[8] if error_line_split[8]!='None' else 'None'
        else:
            error_line_split[7] = (
                int(error_line_split[7]) * 1000 + int(error_line_split[8])
                if error_line_split[8] != "None"
                else int(error_line_split[7])*1000
            )
        error_line_split[8] = (
            int(error_line_split[9]) if error_line_split[9] != "None" else "None"
        )
        error_line_split[9] = (
            int(error_line_split[10]) if error_line_split[10] != "None" else "None"
        )
        error_line_split[10] = (
            int(error_line_split[11]) if error_line_split[11] != "None" else "None"
        )
        error_line_split[11] = (
            int(error_line_split[12]) if error_line_split[12] != "None" else "None"
        )
        error_line_split[12] = ""
        error_line_split.pop()
        fix_error_lines.append(error_line_split)
    df_error = pd.DataFrame([fix_error_line for fix_error_line in fix_error_lines])
    df_not_error = pd.DataFrame([line.split(",") for line in not_error_lines])
    # Hiển thị các dòng gây lỗi
    print("Các dòng gây lỗi:")
    print(df_error)

    # Lưu lại file CSV đã chỉnh sửa
    df_error.to_csv("fixed_merged.csv", index=False)
    print("File CSV đã được chỉnh sửa đã được lưu vào 'fixed_merged.csv'.")
    df_not_error.to_csv("not_error.csv", index=False)
    print("File CSV đã được chỉnh sửa đã được lưu vào 'not_error.csv'.")

# Nếu không có lỗi, hiển thị nội dung của DataFrame
else:
    print(df.head())
'''
# Đọc dữ liệu từ file CSV
df_a = pd.read_csv("../mojo/data/all_movie_mojo.csv", dtype={"country": object})
df_b = pd.read_csv("../the_numbers/data/all_the-numbers.csv")

# Thêm cột genres cho df_b với giá trị ""
df_b["genres"] = ""

print(df_a.info())
print(df_b.info())
# Gộp dữ liệu từ hai DataFrame
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
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
cols_to_compare = ["month", "year", "mpaa"]
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
    "international_box_office",
    "worldwide_box_office",
]
for col in cols_to_get_greater:
    merged_df[col] = merged_df.apply(
        lambda row: choose_greater_value(row[f"{col}_a"], row[f"{col}_b"]), axis=1
    )

# Sử dụng cột country của df_b cho merged_df
merged_df["country"] = merged_df["country_b"]
merged_df["genres"] = merged_df["genres_a"]

print(merged_df.info())

# Loại bỏ các cột dư thừa
columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)

# Lưu kết quả vào file mới
print(merged_df.info())
merged_df.to_csv("merged.csv", index=False)

print("Tổng hợp dữ liệu thành công và lưu vào file 'merged.csv'.")
