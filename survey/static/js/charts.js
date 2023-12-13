// Chart rendering script
{% for question in questions %}
var ctx_{{ question.id }} = document.getElementById('chart_{{ question.id }}').getContext('2d');
var chart_{{ question.id }} = new Chart(ctx_{{ question.id }}, {
    type: 'bar',
    data: {
        labels: [{% for option in question.option_set.all %}"{{ option.text }}",{% endfor %}],
        datasets: [{
            label: 'Responses',
            data: [{% for option in question.option_set.all %}{{ option.percent }},{% endfor %}],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Create a download button for each chart
var downloadButton_{{ question.id }} = document.createElement('a');
downloadButton_{{ question.id }}.href = chart_{{ question.id }}.toBase64Image();
downloadButton_{{ question.id }}.download = 'chart_{{ question.id }}.png';
downloadButton_{{ question.id }}.textContent = 'Download Chart';
downloadButton_{{ question.id }}.classList.add('ui', 'primary', 'button');
document.getElementById('chart_{{ question.id }}').parentNode.appendChild(downloadButton_{{ question.id }});
{% endfor %}

