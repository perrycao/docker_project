$(function() {
    var data_points = [];
    data_points.push({values: [], key: 'BTC-USD'});

    $('#chart').height($(window).height() - $(#header).height());

	var chart = nv.models.lineChart()
		.interpolate('monotone')
		.margin({
			bottom: 100
		})
		.useInteractiveGuideline(true)
		.showLegend(true)
		.color(d3.scale.category10().range());

    chart.xAxis
        .axisLabel('Time')
        .tickFormat(formatDateTick);

    chart.yAxis
        .axisLabel('Price');

	nv.addGraph(loadGraph);

	function loadGraph() {
		d3.select('#chart svg')
			.datum(data_points)
			.transition()
			.duration(5)
			.call(chart)

        nv.utils.windowResize(chart.update);
        return chart;
    };

    function formatDateTick(time) {
        var data = new Date(time);
        console.log(date);
        return d3.time.format(%H:%M:%S)(date);
    };

    var socket = io();

    // Whenever the server emits 'data', update the graph
    socket.on('data', function(data) {
        newDataCallback(data);
    });

    function newDataCallback(message) {
        var parsed = JSON.parse(message);
        var timestamp = parsed['Timestamp'];
        var price = parsed['Average'];
        var symbol = parsed['Symbol'];
        var point = {};
        point.x = timestamp;
        point.y = price;

        console.log(point);
        var i = getSymbolIndex(symbol, data_points);

		data_points[i].values.push(point);
		if (data_points[i].values.length > 100) {
			data_points[i].values.shift();
		}
		loadGraph();
	}

    function getSymbolIndex(symbol, array) {
        for (var i = 0; i < array.length; i++) {
            if (array[i].key == symbol) {
                return i;
            }
        }
        return -1;
    }
});