import re

# Chuỗi ban đầu
original_string = "Based on 1 User Ratings"

# Sử dụng biểu thức chính quy để tìm số trong chuỗi
number_match = re.search(r'\d{1,3}(?:,\d{3})*', original_string)

# Kiểm tra xem số đã được tìm thấy hay không
if number_match:
    # Lấy số từ kết quả của biểu thức chính quy và loại bỏ dấu phẩy
    number = number_match.group().replace(',', '')
    # In số đã lấy được
    print(number)
else:
    print("Không tìm thấy số trong chuỗi")
