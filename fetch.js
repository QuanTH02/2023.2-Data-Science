fetch('https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/all-time/101')
  .then(response => {
    // Kiểm tra xem phản hồi có thành công không (status code 200 là thành công)
    if (!response.ok) {
      console.error('Failed to retrieve data from API');
      return;
    }
    // Trả về dữ liệu từ phản hồi ở định dạng JSON
    return response.json();
  })
  .then(data => {
    if (data) {
      // Xử lý dữ liệu theo nhu cầu của bạn
      console.log(data);
    }
  })
  .catch(error => {
    console.error(error);
  });
