
$(document).ready(function(){

	var data = {
		username: sessionStorage.getItem("username")
	}

	post("/get_balances", data, function(response){
		console.log(response[0][0])
			balance_data = response;
			var table = document.getElementById("myTable");
			for(let i = 0; i < 10; i++){
				var row = table.insertRow(1)
				var cell1 = row.insertCell(0);
    			var cell2 = row.insertCell(1);
    			cell1.innerHTML = response[i][0];
    			cell2.innerHTML = response[i][1];
    		}
	});

	post("/get_transaction_history", data, function(response){
		console.log(response[0][0])
		transaction_data = response;
		var table = document.getElementById("transactionTable");
		
		for(let i = 0; i < 10; i++){
			var row = table.insertRow(1)
			var cell0 = row.insertCell(0);
			var cell1 = row.insertCell(1);
			var cell2 = row.insertCell(2);
			var cell3 = row.insertCell(3);
			var cell4 = row.insertCell(4);

			cell0.innerHTML = response[i][7];
			cell1.innerHTML = response[i][3];
			cell2.innerHTML = response[i][4];
			cell3.innerHTML = response[i][5];
			cell4.innerHTML = response[i][6];
		}
	});
});

