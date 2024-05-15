function processData2(csvData, backgroundColor, genre) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            const movieCountsByRating = {};

            data.forEach(row => {
                if (row.genres && row.genres.includes(genre)) {
                    let rating = row.ratings;

                    if (rating in movieCountsByRating) {
                        movieCountsByRating[rating]++;
                    } else {
                        movieCountsByRating[rating] = 1;
                    }
                }
            });

            const years = Object.keys(movieCountsByRating);
            const movieCounts = years.map(year => movieCountsByRating[year]);

            drawChart2(years, movieCounts, backgroundColor);

        }
    });
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
