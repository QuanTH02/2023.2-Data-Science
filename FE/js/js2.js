function processData2(csvData, backgroundColor) {
    const rows = csvData.split('\n');

    const movieCountsByRating = {};

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

        if (rating in movieCountsByRating) {
            movieCountsByRating[rating]++;
        } else {
            movieCountsByRating[rating] = 1;
        }
    }

    const years = Object.keys(movieCountsByRating);
    const movieCounts = years.map(year => movieCountsByRating[year]);

    drawChart2(years, movieCounts, backgroundColor);
}

function drawChart2(ratings, movieCounts, backgroundColor) {
    if (currentChart2) {
        currentChart2.destroy();
    }
    const sortedRatings = ratings.slice().sort((a, b) => a - b);

    const sortedMovieCounts = sortedRatings.map(rating => {
        const index = ratings.indexOf(rating);
        return movieCounts[index];
    });

    const movieData = {
        labels: sortedRatings,
        datasets: [{
            label: 'Number of Movies Rated',
            backgroundColor: backgroundColor,
            data: sortedMovieCounts
        }]
    };

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
