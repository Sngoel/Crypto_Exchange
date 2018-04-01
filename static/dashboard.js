//This file contains the JavaScript for dashboard.html

var tableTimer;
var username;

$(document).ready(function(){

	username = sessionStorage.getItem("username");
	

	get("/get_orders", function(response){
		console.log(response);
	});

	//Create HTML table
	var columns = 4;
	var rows = 16;

	for(let i = 0; i < rows; i++){
		var rowNode = document.createElement("TR");
		for(let j = 0; j < columns; j++){
			var dataCellNode = document.createElement("TD");
			var textNode = document.createTextNode("Test");
			dataCellNode.appendChild(textNode);
			rowNode.appendChild(dataCellNode);
		}
		document.getElementById("bid_table").appendChild(rowNode);
	}


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


	var currentIndex = 0;
	var shiftBy = 4;
	var secondsBetweenUpdates = 1;

	//This is the function that's called every x seconds to update the table
	var updateTable = function(){
		var currentRow = $("tr").first();
		for(let i = 0; i < rows; i++){

			var currentCell = currentRow.children().first();

			currentCell.text(orders[currentIndex + i].coin1);
			currentCell = currentCell.next();
			currentCell.text(orders[currentIndex + i].amount1);
			currentCell = currentCell.next();
			currentCell.text(orders[currentIndex + i].coin2);
			currentCell = currentCell.next();
			currentCell.text(orders[currentIndex + i].amount2);

			currentRow = currentRow.next();
		}
		currentIndex += shiftBy;
	}

	//Call updateTable() every secondsBetweenUpdates seconds
	tableTimer = window.setInterval(updateTable, secondsBetweenUpdates * 1000);


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

var getOrderBook = function(){
	$.get("/dashboard/test", function(response){
		console.log(response);
	});
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