function processData(csvData, backgroundColor) {
    // Chuyển đổi dữ liệu CSV thành mảng các dòng
    const rows = csvData.split('\n');

    // Khởi tạo đối tượng lưu trữ số phim theo từng năm
    const movieCountsByYear = {};

    // Lặp qua từng dòng dữ liệu (trừ dòng tiêu đề)
    for (let i = 1; i < rows.length; i++) {
        let year;
        if (rows[i].includes('"')) {
            const row = rows[i].split('"');
            const r = row[2].split(',');
            year = parseInt(r[2]);
        } else {
            const row = rows[i].split(',');
            year = parseInt(row[5]);
        }

        if (year < 1900) continue;
        if (!year) continue;

        // Tăng số lượng phim theo năm tương ứng
        if (year in movieCountsByYear) {
            movieCountsByYear[year]++;
        } else {
            movieCountsByYear[year] = 1;
        }
    }

    // Chuyển đổi dữ liệu thành định dạng phù hợp cho biểu đồ
    const years = Object.keys(movieCountsByYear);
    const movieCounts = years.map(year => movieCountsByYear[year]);

    // Vẽ biểu đồ
    drawChart(years, movieCounts, backgroundColor);
}

function drawChart(years, movieCounts, backgroundColor) {
    if (currentChart) {
        currentChart.destroy();
    }
    // Dữ liệu đồ thị
    const movieData = {
        labels: years,
        datasets: [{
            label: 'Number of Movies Released',
            backgroundColor: backgroundColor,
            data: movieCounts
        }]
    };

    // Tạo đồ thị cột
    const ctx = document.getElementById('bar-chart').getContext('2d');
    currentChart = new Chart(ctx, {
        type: 'line',
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