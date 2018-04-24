//This file contains the JavaScript for dashboard.html


//Globals and configuration variables
var current_coin = "XRP";


var tableTimer;
var username;
var order_data = [];




var currentIndex = 0;
var shiftBy = 2;
var secondsBetweenUpdates = 1;

$(document).ready(function(){

	//If user is not currently logged in, redirect to landing page
	check_if_logged_in();

	username = sessionStorage.getItem("username");
	//console.log(username);
	

	//Get order data for table from server
	post("/get_orders", {coin_type: current_coin}, function(response){

		console.log(response);


		/***********************************************
			Now that order data is correctly formatted:
				1. Create an HTML table
				2. Add order data to table
		************************************************/
		

		var table_html = '';

		table_html += ` <thead>
							<tr>
								<th scope = "col">#</th>
								<th scope = "col">` + current_coin + `</th>
								<th scope = "col">` + current_coin + `/BTC</th>
							</tr>
						</thead>
						<tbody>`

		for(let i = 0; i < response.length; i++){

			table_html +=  `<tr>
						   		<th scope = "row">` + (i + 1) + `</th>
								<td>` + response[i].order_amount + `</td>
								<td>` + response[i].order_price + `</td>
							</tr>`;

		}



		table_html += "</tbody>";

		//console.log(table_html);

		document.getElementById("order_table").innerHTML = table_html;
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
	



var submit_order = function(){

	var coin_type = document.getElementById("coin_type").value;
	var order_amount = document.getElementById("order_amount").value;
	var order_price = document.getElementById("order_price").value;
	var order_type = document.getElementById("order_type").value;

	if(coin_type === "Empty"){
		alert("Please select a coin type");
	}
	
	else if(order_amount === "" || isNaN(order_amount) || parseInt(order_amount) <= 0){
		alert("Please enter a valid order amount");
	}

	else if(order_price === "" || isNaN(order_price)|| parseInt(order_price) <= 0){
		alert("Please enter a valid order amount");
	}

	else{

	    var order_info = {
	    	username: sessionStorage.getItem("username"),
			order_amount : order_amount,
			order_price : order_price,
			order_type : order_type,
			coin_type: coin_type
	    };

	    post('/submit_order', order_info, function(response){

	    	if(response === "insufficient funds"){
	    		alert("You have insufficient funds for this transaction; transaction was canceled");
	    	}

	    	else if(response === "order added"){
	    		alert("Your order was added to the database");
	    	}

	    	else if(response === "order completed"){
	    		alert("Your order was successfully completed");
	    	}
	    });
	}
}

