(function ($) {
	"use strict";
	var DemoCharts = function () {
		// Create reference to this instance
		var o = this;
		// Initialize app when document is ready
		$(document).ready(function () {
			o.initialize();
		});

	};
	var p = DemoCharts.prototype;

	function _drawFlotChart(divName, jsonData) {
		var chart = $(divName);
		if (!$.isFunction($.fn.plot) || chart.length === 0) {
			return;
		}

		var o = this;
		var labelColor = chart.css('color');
		var data = [jsonData];

		var options = {
			colors: chart.data('color').split(','),
			series: {
				shadowSize: 0,
				lines: {
					show: true,
					lineWidth: 2
				},
				points: {
					show: true,
					radius: 3,
					lineWidth: 2
				}
			},
			legend: {
				show: false
			},
			xaxis: {
				tickDecimals: 0,
				color: 'rgba(0, 0, 0, 0)',
				font: {color: labelColor}
			},
			yaxis: {
				font: {color: labelColor}
			},
			grid: {
				borderWidth: 0,
				color: labelColor,
				hoverable: true
			}
		};

		chart.width('100%');
		var plot = $.plot(chart, data, options);

		var tip, previousPoint = null;
		chart.bind("plothover", function (event, pos, item) {
			if (item) {
				if (previousPoint !== item.dataIndex) {
					previousPoint = item.dataIndex;

					var x = item.datapoint[0];
					var y = item.datapoint[1];
					var tipLabel = '<strong>' + $(this).data('title') + '</strong>';
					var tipContent = y + " " + item.series.label.toLowerCase();

					if (tip !== undefined) {
						$(tip).popover('destroy');
					}
					tip = $('<div></div>').appendTo('body').css({left: item.pageX, top: item.pageY - 5, position: 'absolute'});
					tip.popover({html: true, title: tipLabel, content: tipContent, placement: 'top'}).popover('show');
				}
			}
			else {
				if (tip !== undefined) {
					$(tip).popover('destroy');
				}
				previousPoint = null;
			}
		});
	};

	p.initialize = function () {
		// Flot
		// this._initFlotLine();
	};

	function _drawMorrisAreaChart(divName, jsonData) {
		if (typeof Morris !== 'object') {
			return;
		}
		// Morris Area demo
		if ($(divName).length > 0) {
			var labelColor = $(divName).css('color');
			Morris.Area({
				element: divName,
				behaveLikeLine: true,
				data: [
					{x: '2011 Q1', y: 3, z: 3},
					{x: '2011 Q2', y: 2, z: 1},
					{x: '2011 Q3', y: 2, z: 4},
					{x: '2011 Q4', y: 3, z: 3}
				],
				xkey: 'x',
				ykeys: ['y', 'z'],
				labels: ['Y', 'Z'],
				gridTextColor: labelColor,
				lineColors: $(divName).data('colors').split(',')
			});
		}
	};

	$.drawFlotChart = function(placeholder, jsonData) {
        var drawFlotChart = new _drawFlotChart($(placeholder), jsonData);
        return drawFlotChart;
    };

    $.drawMorrisAreaChart = function(placeholder, jsonData) {
        var drawMorrisAreaChart = new _drawMorrisAreaChart($(placeholder), jsonData);
        return drawMorrisAreaChart;
    };
	// =========================================================================
	
}(jQuery));
