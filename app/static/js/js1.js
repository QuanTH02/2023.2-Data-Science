function processData(csvData, backgroundColor, genre) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            const movieCountsByYear = {};

            data.forEach(row => {
                if (row.genres && row.genres.includes(genre)) {
                    
                    const year = row.year;

                    if (year in movieCountsByYear) {
                        movieCountsByYear[year]++;
                    } else {
                        movieCountsByYear[year] = 1;
                    }
                }
            });

            const years = Object.keys(movieCountsByYear);
            const movieCounts = years.map(year => movieCountsByYear[year]);

            drawChart(years, movieCounts, backgroundColor);
        }
    });
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