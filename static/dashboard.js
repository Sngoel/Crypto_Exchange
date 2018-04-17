//This file contains the JavaScript for dashboard.html


//Globals and configuration variables
var tableTimer;
var username;
var order_data = [];


var columns = 3;
var rows = 16;


var currentIndex = 0;
var shiftBy = 2;
var secondsBetweenUpdates = 1;

$(document).ready(function(){

	username = sessionStorage.getItem("username");
	//console.log(username);


	//Get order data for table from server
	get("/get_orders", function(response){

		order_data = response;


		/***********************************************
			Now that order data is correctly formatted:
				1. Create an HTML table
				2. Add order data to table
		************************************************/

		//Create HTML table
		for(let i = 0; i < rows; i++){
			var rowNode = document.createElement("TR");
			for(let j = 0; j < columns; j++){
				var dataCellNode = document.createElement("TD");

				var column_mapping = [4, 2, 5];

				var text = order_data[i][column_mapping[j]];

				/*var text;
				if(j == 0){
					text = order_data[i][4];
				}

				else if(j == 1){
					text = order_data[i][2];
				}

				else if(j == 2){
					text = order_data[i][5];
				}*/

				var textNode = document.createTextNode(order_data[i][column_mapping[j]]);
				dataCellNode.appendChild(textNode);
				rowNode.appendChild(dataCellNode);
			}
			document.getElementById("order_table").appendChild(rowNode);
		}


		//Call updateTable() every secondsBetweenUpdates seconds
		tableTimer = window.setInterval(updateTable, secondsBetweenUpdates * 1000);
	});


	//Sample graph to build off of
	TESTER = document.getElementById('graph');
	Plotly.plot(TESTER, [{
		x: [1, 2, 3, 4, 5],
		y: [1, 2, 4, 8, 16]
	}], {
		margin: {
		t: 0
	}});
}); 	//end of document.ready


//This is the function that's called every x seconds to update the table
var updateTable = function(){
	var currentRow = $("tr").first();
	for(let i = 1; i < rows; i++){

		var currentCell = currentRow.children().first();

		currentCell.text(order_data[currentIndex + i][4]);
		currentCell = currentCell.next();
		currentCell.text(order_data[currentIndex + i][2]);
		currentCell = currentCell.next();
		currentCell.text(order_data[currentIndex + i][5]);

		currentRow = currentRow.next();
	}
	currentIndex += shiftBy;
}


var pauseData = function(){
	clearInterval(tableTimer);
}


var place_order = function(){

    var order_info = {
			username: sessionStorage.getItem("username"),
			order_type : document.getElementById('order_type').value,
			coin_id : document.getElementById('coin_id_main').value,
			amount : document.getElementById('price').value
    };
			console.log(order_info)

    post('/submit_order', order_info, function(response){
    	console.log(response)
    });
}


//Select your cryptocurrency to search_bar:
// Drop down Button"



var search = function(){

	var search = document.getElementById('search_text').value

	post('/search', {search_text:search}, function(response){
		console.log(response)
	});
}
