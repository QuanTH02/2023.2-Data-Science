function processData3(csvData, backgroundColor) {
    const rows = csvData.split('\n');

    let revenue = [];
    let budget = [];

    for (let i = 1; i < rows.length; i++) {
        let year;
        if (rows[i].includes('"')) {
            const row = rows[i].split('"');
            const r = row[2].split(',');
            budget.push(parseInt(r[4])); 
            revenue.push(parseInt(r[8])); 
        } else {
            const row = rows[i].split(',');
            budget.push(parseInt(row[7])); 
            revenue.push(parseInt(row[11])); 
        }
    }

    drawChart3(budget, revenue, backgroundColor);
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

