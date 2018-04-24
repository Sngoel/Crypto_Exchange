$(document).ready(function(){

	//If user is not currently logged in, redirect to landing page
	check_if_logged_in();

	var data = {
		search_text: sessionStorage.getItem("search_text")
	}

	post('/search', data, function(response){
        console.log(response);

		var total_html = '';
		total_html += '<ul id = "questions" class="list-group" style = "width: 80%; margin: 0% 0% 0% 10%;">';

		for(let i = 0; i < response.length; i++){

			var complete_question_div = ""

			complete_question_div += '<li class = "list-group-item" onclick = "select_thread(event)" id = "';
			complete_question_div += response[i].question_id + '">' + response[i].question_summary;
			complete_question_div += '<span class="badge">' + response[i].vote_count + '</span></li>';
			
			total_html += complete_question_div;
		}

		total_html += '</ul><br><br>';
		document.body.innerHTML += total_html;
    });
});


var select_thread = function(){
	sessionStorage.setItem("question_id", event.target.id);
	window.location = "/thread";
}



