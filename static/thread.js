


$(document).ready(function(){

	var data = {
		username: sessionStorage.getItem("username"),
		question_id: sessionStorage.getItem("question_id")
	}

	post("/load_thread", data, function(response){

		console.log(response);


		var question_html = '';
		question_html += '<div id = "question_container"><div id = "vote_and_summary_container">';
		question_html += '<div class = "vote_container"><div id = "question_vote_count">';
		question_html += response.question_vote_count[0] + '</div>';
		question_html += '<div class = "vote_buttons_container">';
		question_html += '<input type = "button" class = "vote_button" value = "Upvote">';
		question_html += '<input type = "button" class = "vote_button" value = "Downvote">';
		question_html += '</div></div><div id = "question_summary">';
		question_html += response.question_info[0][2] + '</div></div>';
		question_html += '<div id = "question_description_container"><div id = "question_description">';
		question_html += response.question_info[0][3] + '</div></div></div>';


		document.body.innerHTML += question_html;

		for(let i = 0; i < response.comments.length; i++){
			var comment_html = '';
			comment_html += '<div class = "comment_container"><div class = "vote_container">';
			comment_html += '<div class = "vote_count_container">'
			comment_html += response.comment_vote_counts[i][1] + '</div><div class = "vote_buttons_container">';
			comment_html += '<input type = "button" class = "vote_button" value = "Upvote">';
			comment_html += '<input type = "button" class = "vote_button" value = "Downvote">';
			comment_html += '</div></div><div class = "comment_text_container">'
			comment_html += response.comments[i][3] + '</div></div>';
			document.body.innerHTML += comment_html;
		}
	});
});


