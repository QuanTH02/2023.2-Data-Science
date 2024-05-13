function processData2(csvData, backgroundColor) {
    // Chuyển đổi dữ liệu CSV thành mảng các dòng
    const rows = csvData.split('\n');

    // Khởi tạo đối tượng lưu trữ số phim theo từng năm
    const movieCountsByRating = {};

    // Lặp qua từng dòng dữ liệu (trừ dòng tiêu đề)
    for (let i = 1; i < rows.length; i++) {
        let rating;
        if (rows[i].includes('"')) {
            const row = rows[i].split('"');
            const r = row[2].split(',');
            rating = (r[3]);
        } else {
            const row = rows[i].split(',');
            rating = (row[3]);
        }

        if (!rating) continue;

        // Tăng số lượng phim theo năm tương ứng
        if (rating in movieCountsByRating) {
            movieCountsByRating[rating]++;
        } else {
            movieCountsByRating[rating] = 1;
        }
    }

    // Chuyển đổi dữ liệu thành định dạng phù hợp cho biểu đồ
    const years = Object.keys(movieCountsByRating);
    const movieCounts = years.map(year => movieCountsByRating[year]);

    // Vẽ biểu đồ
    drawChart2(years, movieCounts, backgroundColor);
}

function drawChart2(ratings, movieCounts, backgroundColor) {
    if (currentChart2) {
        currentChart2.destroy();
    }
    // Sắp xếp dữ liệu theo thứ tự tăng dần của ratings
    const sortedRatings = ratings.slice().sort((a, b) => a - b);

    // Tạo một mảng mới chứa các movieCounts tương ứng với thứ tự sắp xếp của ratings
    const sortedMovieCounts = sortedRatings.map(rating => {
        const index = ratings.indexOf(rating);
        return movieCounts[index];
    });

    // Dữ liệu đồ thị
    const movieData = {
        labels: sortedRatings,
        datasets: [{
            label: 'Number of Movies Rated',
            backgroundColor: backgroundColor,
            data: sortedMovieCounts
        }]
    };

    // Tạo đồ thị cột
    const ctx = document.getElementById('bar2-chart').getContext('2d');
    currentChart2 = new Chart(ctx, {
        type: 'bar',
        data: movieData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
