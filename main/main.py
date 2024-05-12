import pandas as pd

# Đọc dữ liệu từ hai tệp CSV
mojo_df = pd.read_csv('../mojo/data/test_mojo.csv')
thenumber_df = pd.read_csv('../the-numbers/data/update_month/test_the_numbers.csv')

# Gộp hai DataFrame theo trường 'movie_name'
merged_df = pd.merge(mojo_df, thenumber_df, on='movie_name', how='outer')

# Loại bỏ các bản ghi trùng lặp dựa trên trường 'movie_name'
merged_df.drop_duplicates(subset='movie_name', inplace=True)

# Lưu DataFrame đã tổng hợp và loại bỏ các bản ghi trùng vào một tệp CSV mới
merged_df.to_csv('merged_data.csv', index=False)