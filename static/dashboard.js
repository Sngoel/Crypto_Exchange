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
	

	//Get order data for table from server
	get("/get_orders", function(response){

		//Data comes back as a string, so store correctly formatted data in "order_data"
		array_of_strings = response.split("], [");

		for(let i = 0; i < array_of_strings.length; i++){
			order_data.push(array_of_strings[i].split(", "));
		}

		for(let i = 0; i < order_data.length; i++){
			for(let j = 0; j < order_data[i].length; j++){
				order_data[i][j] = order_data[i][j].replace(/[\[\]"]+/g, '');
			}
		}


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

				//var textNode = document.createTextNode(order_data[i][column_mapping[j]]);


				var text;
				if(j == 0){
					text = order_data[i][4];
				}

				else if(j == 1){
					text = order_data[i][2];
				}

				else if(j == 2){
					text = order_data[i][5];
				}

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
	for(let i = 0; i < rows; i++){

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


var place_order = function(order_type){

    var order_info = {
		amount : document.getElementById('amount').value,
		price : document.getElementById('price').value,
		order_type : order_type
    };

    post('/submit_order', order_info, function(response){
    	console.log(response)
    });
}


//POST wrapper function
var post = function(url, data, callback){
        $.ajax({
        type : "POST",
        url : url,
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
        callback(response);
        }
        });
}


//GET wrapper function
var get = function(url, callback){
    $.ajax({
        type : "GET",
        url : url,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
        	callback(response);
        }
    });
}




/*
//Generate data
var coins = ["BTC", "ETH", "LTC", "XRP", "NEO"];
var orderLimit = 1000;
var orders = [];
for(let i = 0; i < orderLimit; i++){
	var coinIndex = Math.floor(Math.random() * coins.length);
	orders.push({
		coin1: coins[coinIndex],
		amount1: Math.floor(Math.random() * 100),
		coin2: coins[coins.length - 1 - coinIndex],
		amount2: Math.floor(Math.random() * 100)
	});
	//console.log(orders[orders.length - 1]);
}
*/