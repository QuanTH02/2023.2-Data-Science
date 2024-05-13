function processData3(csvData, backgroundColor) {
    // Chuyển đổi dữ liệu CSV thành mảng các dòng
    const rows = csvData.split('\n');

    // Khởi tạo mảng lưu trữ số phim theo từng năm
    let revenue = [];
    let budget = [];

    // Lặp qua từng dòng dữ liệu (trừ dòng tiêu đề)
    for (let i = 1; i < rows.length; i++) {
        let year;
        if (rows[i].includes('"')) {
            const row = rows[i].split('"');
            const r = row[2].split(',');
            budget.push(parseInt(r[4])); // Sử dụng push() thay vì append()
            revenue.push(parseInt(r[8])); // Sử dụng push() thay vì append()
        } else {
            const row = rows[i].split(',');
            budget.push(parseInt(row[7])); // Sử dụng push() thay vì append()
            revenue.push(parseInt(row[11])); // Sử dụng push() thay vì append()
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

    // Tùy chọn của biểu đồ
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

    // Vẽ biểu đồ
    const ctx = document.getElementById('bar3-chart').getContext('2d');
    currentChart3 = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: options
    });
}

