$(document).ready(function(){

	post("/get_questions", {category: "all"}, function(response){

		var question_template = {
			beginning: '<div id = "',
			middle1: '" class = "question_container" onclick = "select_thread(event)">',
			end: '</div>'
		};

		for(let i = 0; i < response.length; i++){

			var complete_question_div = ""
			complete_question_div += question_template.beginning;
			complete_question_div += response[i][0];
			complete_question_div += question_template.middle1;
			complete_question_div += response[i][2];
			complete_question_div += question_template.end;

			document.body.innerHTML += complete_question_div;
		}
	});
});


var select_thread = function(){
	sessionStorage.setItem("question_id", event.target.id);
	window.location = "/thread";
}



