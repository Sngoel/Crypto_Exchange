

$(document).ready(function(){

	var question_id = sessionStorage.getItem("question_id");

	post("/load_thread", {question_id: question_id}, function(response){

		console.log(response);

		for(let i = 0; i < response.length; i++){
			var comment_html = '';
			comment_html += '<div class = "comment_container"><div class = "vote_container">';
			comment_html += '<div class = "vote_count_container">166&nbsp;</div><div class = "vote_buttons_container">';
			comment_html += '<input type = "button" class = "vote_button" value = "Upvote">';
			comment_html += '<input type = "button" class = "vote_button" value = "Downvote">';
			comment_html += '</div></div><div class = "comment_text_container">'
			comment_html += response[i][3] + '</div></div>';
			document.body.innerHTML += comment_html;
		}
	});
});


