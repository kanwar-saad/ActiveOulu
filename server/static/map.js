var devices;
var activity;
var map, pointarray, heatmap, serverData;
var heatmapData = [];

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


function get_activity()
{
	var dict2 = null;
	$.ajax({
		'async': false,
		'global': false,
		'url': "/api/bt_activity",
		'dataType': "json",
		'success': function (data) {
			dict2 = data;
		}
	});
	activity =  dict2;
}

function heatmapdata()
{
	heatmapData = [];
	for (var i = 0; i < devices.devices.length; i++) 
  	{
		var latLng = new google.maps.LatLng(devices.devices[i].latitude, devices.devices[i].longitude);
		var magnitude = activity.activity[i].count;
		
		if (magnitude)
		{
			//alert(magnitude.toString());
			var weightedLoc = {location: latLng, weight: magnitude};
			heatmapData.push(weightedLoc);
		}
	}
}

function reload_heat_layer()
{
	get_activity()
	heatmapdata();

	pointArray = new google.maps.MVCArray(heatmapData);
	heatmap.setData(pointArray);
	heatmap.setMap(null);
	heatmap.setMap(map);

}
 
function initialize() 
{	
	get_devices();
	var mapOptions = 
	{
	  center: new google.maps.LatLng(+65.007714, +25.462874),
	  zoom: 14,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
	
	heatmap = new google.maps.visualization.HeatmapLayer();
	heatmap.setOptions({radius:20});
	reload_heat_layer();
	//setInterval(reload_heat_layer, 3000);
}



