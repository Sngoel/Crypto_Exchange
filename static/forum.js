$(document).ready(function(){

	//If user is not currently logged in, redirect to landing page
	check_if_logged_in();

	post("/get_questions", {category: "all"}, function(response){

		console.log(response);

		var question_info = [];

		//Match up question summaries and votes
		for(let i = 0; i < response.questions.length; i++){

			var found = false;

			for(let j = 0; j < response.question_votes.length; j++){

				if(response.questions[i][0] === response.question_votes[j][0]){

					found = true;
					question_info.push({
						question_id: response.questions[i][0],
						question_summary: response.questions[i][1],
						question_vote_total: response.question_votes[j][1]
					});
					break;
				}
			}

			if(!found){
				question_info.push({
					question_id: response.questions[i][0],
					question_summary: response.questions[i][1],
					question_vote_total: 0
				});
			}

		}

		var total_html = '';
		total_html += '<ul class="list-group" style = "width: 80%; margin: 0% 0% 0% 10%;">';

		for(let i = 0; i < question_info.length; i++){

			var complete_question_div = ""

			complete_question_div += '<li class = "list-group-item" onclick = "select_thread(event)" id = "';
			complete_question_div += question_info[i].question_id + '">' + question_info[i].question_summary;
			complete_question_div += '<span class="badge">' + question_info[i].question_vote_total + '</span></li>';
			
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



