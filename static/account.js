
$(document).ready(function(){

	var data = {
		username: sessionStorage.getItem("username")
	}

	post("/get_balances", data, function(response){

		console.log(response);
		var balances = response;

		var table_html = `	<thead>
								<tr>
									<th scope = "col">#</th>
									<th scope = "col">Coin</th>
									<th scope = "col">Balance</th>
								</tr>
							</thead>
							<tbody>`

		for(let i = 0; i < balances.length; i++){
			table_html +=  `<tr>
								<th scope = "row">` + (i + 1) + `</th>
								<td>` + balances[i].coin_id + `</td>
								<td>` + balances[i].coin_balance + `</td>
							</tr>`;
		}

		table_html += "</tbody>";
		document.getElementById("balance_table").innerHTML = table_html;
	});


	post("/get_transaction_history", data, function(response){

		console.log(response)
		var transactions = response;

		var table_html = `	<thead>
								<tr>
									<th scope = "col">#</th>
									<th scope = "col">Date</th>
									<th scope = "col">Coin</th>
									<th scope = "col">Order Type</th>
									<th scope = "col">Amount</th>
									<th scope = "col">Price</th>
								</tr>
							</thead>
							<tbody>`


		for(let i = 0; i < transactions.length; i++){
			table_html +=  `<tr>
								<th scope = "row">` + (i + 1) + `</th>
								<td>` + transactions[i].time + `</td>
								<td>` + transactions[i].coin_id + `</td>
								<td>` + transactions[i].order_type + `</td>
								<td>` + transactions[i].amount + `</td>
								<td>` + transactions[i].price + `</td>
							</tr>`;
		}

		table_html += "</tbody>";
		document.getElementById("transaction_table").innerHTML = table_html;

	});
});

