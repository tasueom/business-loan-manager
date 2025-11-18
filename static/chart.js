// 차트 데이터 가져오기 (data attribute에서)
const chartDataElement = document.getElementById('chart-data');
const chartData = JSON.parse(chartDataElement.getAttribute('data-chart'));

// 차트 생성
const ctx = document.getElementById('loan-chart');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartData.labels,
        datasets: [{
            label: '총 상환액',
            data: chartData.values,
            backgroundColor: 'rgba(76, 175, 80, 0.6)',
            borderColor: 'rgba(76, 175, 80, 1)',
            borderWidth: 2,
            borderRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            title: {
                display: true,
                text: '대출 상환액 차트',
                font: {
                    size: 18,
                    weight: 'bold'
                },
                padding: {
                    top: 10,
                    bottom: 20
                }
            },
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                callbacks: {
                    afterLabel: function(context) {
                        const index = context.dataIndex;
                        const tooltip = chartData.tooltips[index];
                        return [
                            '회사명: ' + (tooltip.company_name || '없음'),
                            '사업자번호: ' + (tooltip.biz_no || '없음'),
                            '연락처: ' + (tooltip.phone || '없음'),
                            '주소: ' + (tooltip.address || '없음'),
                            '대출금액: ' + (tooltip.loan_amount ? tooltip.loan_amount.toLocaleString() + '원' : '없음'),
                            '대출기간: ' + (tooltip.term_months || 0) + '개월',
                            '연 이율: ' + (tooltip.annual_rate || 0) + '%',
                            '등록일시: ' + (tooltip.created_at || '없음')
                        ];
                    },
                    label: function(context) {
                        return '총 상환액: ' + context.parsed.y.toLocaleString() + '원';
                    }
                },
                padding: 12,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: 'rgba(76, 175, 80, 1)',
                borderWidth: 1
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value.toLocaleString() + '원';
                    }
                },
                title: {
                    display: true,
                    text: '금액 (원)',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            },
            x: {
                title: {
                    display: true,
                    text: '대출 ID',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    }
});

