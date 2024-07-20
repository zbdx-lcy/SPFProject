document.addEventListener('DOMContentLoaded', function() {
    var formulation = JSON.parse(`${formulation}`);
    var temperatures = JSON.parse(`${temperatures}`);
    var relatedData = JSON.parse(`${related_data}`);


// 其余的JavaScript代码...

    var chartData = {};

    temperatures.forEach(function(temperature) {
        var temperatureId = temperature.temp_id;

        var data = relatedData.filter(function(item) {
            return item.temperature_id === temperatureId;
        });

        var timeMin = data.map(function(item) {
            return item.time_min;
        });

        var lossMod = data.map(function(item) {
            return Math.log10(item.loss_mod);
        });

        var energyStorageMod = data.map(function(item) {
            return Math.log10(item.energy_storage_mod);
        });

        chartData[temperatureId] = {
            timeMin: timeMin,
            lossMod: lossMod,
            energyStorageMod: energyStorageMod
        };
    });

    var ctx = document.getElementById('chart_' + formulation.formulation_id).getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData[temperatures[0].temp_id].timeMin,
            datasets: []
        },
        options: {
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var datasetLabel = data.datasets[tooltipItem.datasetIndex].label || '';
                        var value = tooltipItem.yLabel;
                        var index = tooltipItem.index;
                        var temperatureId = data.datasets[tooltipItem.datasetIndex].temperatureId;

                        return datasetLabel + ': ' + value.toFixed(2) + ', Time: ' + chartData[temperatureId].timeMin[index] + ' min';
                    }
                }
            }
        }
    });

    temperatures.forEach(function(temperature) {
        var temperatureId = temperature.temp_id;

        var datasetLossMod = {
            label: 'Temperature ' + temperature.temp_value + '°C',
            data: chartData[temperatureId].lossMod,
            borderColor: getRandomColor(),
            fill: false,
            temperatureId: temperatureId
        };

        var datasetEnergyStorageMod = {
            label: 'Temperature ' + temperature.temp_value + '°C',
            data: chartData[temperatureId].energyStorageMod,
            borderColor: getRandomColor(),
            fill: false,
            temperatureId: temperatureId
        };

        chart.data.datasets.push(datasetLossMod);
        chart.data.datasets.push(datasetEnergyStorageMod);
    });

    chart.update();
});

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
