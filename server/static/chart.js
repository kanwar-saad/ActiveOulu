
var data;
var ac;
var h, w;

var devices;
var history;

function get_devices() 
{
	var dict1 = null;
	$.ajax({
		'async': false,
		'global': false,
		'url': "/api/bt_devices",
		'dataType': "json",
		'success': function (data) {
			dict1 = data;
		}
	});
	devices =  dict1;
}

function get_history(id, time) 
{
	var hist = null;
	var url = "/api/bt_activity_history/";
	if (id != 0)
	{
		url += "?id=" + id;
		if (time != 0)
		{
			url += "&t=" + time;
		}
	}
	
	$.ajax({
		'async': false,
		'global': false,
		'url': url,
		'dataType': "json",
		'success': function (data) {
			hist = data;
		}
	});
	history =  hist;
}


function initChartData() 
{

	h = $("#chart").width(true) * 0.6;
	w = $("#chart").height(true) ;
	// Some raw data (not necessarily accurate)
	data = google.visualization.arrayToDataTable([
	  ['Month',   'Bolivia'],
	  ['2004/05',    165],
	  ['2005/06',    135],
	  ['2006/07',    157],
	  ['2007/08',    139],
	  ['2008/09',    136]
	]);

	// Create and draw the visualization.
	ac = new google.visualization.AreaChart(document.getElementById('visualization'));
}

function drawChart()
{

	ac.draw(data, {
	  title : 'Activity Chart',
	  isStacked: true,
	  legend: {position: 'none'},
	  chartArea: {width: "80%"},
	  vAxis: {title: "Cups"},
	  hAxis: {title: "Month"}
	});
}

function initAndDraw(){
	initChartData();
	drawChart();
}

$(window).resize(function() {
	//w = $("#chart").width(true);
	//h = $("#chart").height(true);
	drawChart();
	}
);	

google.setOnLoadCallback(initAndDraw);

