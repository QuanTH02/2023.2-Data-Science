import requests
from bs4 import BeautifulSoup

# URL của trang web bạn muốn lấy HTML
url = 'https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/all-time/101'

# Gửi yêu cầu HTTP GET đến URL và lấy phản hồi
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công hay không (status code 200 là thành công)
if response.status_code == 200:
    # Lấy nội dung HTML từ phản hồi
    html_content = response.text

    # Sử dụng BeautifulSoup để phân tích HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # In ra HTML của trang web
    print(soup.prettify())
else:
    print('Failed to retrieve HTML content:', response.status_code)
