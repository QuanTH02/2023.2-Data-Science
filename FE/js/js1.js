function processData(csvData, backgroundColor) {
    const rows = csvData.split('\n');

    const movieCountsByYear = {};

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

        if (year in movieCountsByYear) {
            movieCountsByYear[year]++;
        } else {
            movieCountsByYear[year] = 1;
        }
    }

    const years = Object.keys(movieCountsByYear);
    const movieCounts = years.map(year => movieCountsByYear[year]);

    drawChart(years, movieCounts, backgroundColor);
}

function drawChart(years, movieCounts, backgroundColor) {
    if (currentChart) {
        currentChart.destroy();
    }
    const movieData = {
        labels: years,
        datasets: [{
            label: 'Number of Movies Released',
            backgroundColor: backgroundColor,
            data: movieCounts
        }]
    };

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