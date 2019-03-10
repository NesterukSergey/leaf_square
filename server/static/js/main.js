google.charts.load('current', {packages: ['corechart', 'line', 'gauge']});
// google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(startScript());

function requestFormServer(url, data) {
    return new Promise(function (succeed, fail) {
        $.ajax({
            type: "POST",
            url: url,
            data: data || '',
            success: function (response) {
                succeed(JSON.parse(response));
            },
            error: function (error) {
                console.log(error + ' at ' + url);
                fail(error);
            }
        });
    });
}

var sensorData = [];


function getSensorData() {
    requestFormServer('/get_sensor_data', {}).then(function (response) {
        // console.log(JSON.parse(response));

        updateCharts(JSON.parse(response));
    })
    //     .catch(error => {
    //     console.log(error)
    // })
}

