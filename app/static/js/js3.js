function processData3(csvData, backgroundColor, genre) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            let revenue = [];
            let budget = [];

            data.forEach(row => {
                if (row.genres && row.genres.includes(genre)) {
                    const bud = row.budget;
                    const rev = row.domestic_box_office;
                    
                    budget.push(bud);
                    revenue.push(rev);
                }
            });

            drawChart3(budget, revenue, backgroundColor);
        }
    });
}


function drawChart3(budgets, revenues, backgroundColor) {
    if (currentChart3) {
        currentChart3.destroy();
    }

    const data = {
        datasets: [{
            label: 'Revenue',
            data: budgets.map((budget, index) => ({ x: budget, y: revenues[index] })),
            backgroundColor: backgroundColor, // Màu nền của điểm
        }]
    };

    const options = {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Budget'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Revenue'
                }
            }
        }
    };

    const ctx = document.getElementById('bar3-chart').getContext('2d');
    currentChart3 = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: options
    });
}

