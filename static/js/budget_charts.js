document.addEventListener('DOMContentLoaded', function () {
    // Get the budget data from the hidden div
    var budgetDataElement = document.getElementById('budgetData');
    var budgetData = {
        needs: parseFloat(budgetDataElement.dataset.needs),
        wants: parseFloat(budgetDataElement.dataset.wants),
        savings: parseFloat(budgetDataElement.dataset.savings),
        actual_needs: parseFloat(budgetDataElement.dataset.actualNeeds),
        actual_wants: parseFloat(budgetDataElement.dataset.actualWants),
        actual_savings: parseFloat(budgetDataElement.dataset.actualSavings)
    };

    // Pie Chart
    var ctxPie = document.getElementById('budgetPieChart').getContext('2d');
    var budgetPieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: ['Needs', 'Wants', 'Savings'],
            datasets: [{
                data: [budgetData.needs, budgetData.wants, budgetData.savings],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Budget Allocation'
            }
        }
    });

    // Bar Chart
    var ctxBar = document.getElementById('comparisonBarChart').getContext('2d');
    var comparisonBarChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['Needs', 'Wants', 'Savings'],
            datasets: [{
                label: 'Budgeted',
                data: [budgetData.needs, budgetData.wants, budgetData.savings],
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }, {
                label: 'Actual',
                data: [budgetData.actual_needs, budgetData.actual_wants, budgetData.actual_savings],
                backgroundColor: 'rgba(255, 99, 132, 0.5)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            title: {
                display: true,
                text: 'Budget vs. Actual Spending'
            }
        }
    });
});