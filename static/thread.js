var page_info = {
	question_info: {
		id: undefined,
		user_vote: undefined
	},
	comment_info: []
}


$(document).ready(function(){

	//Save off question ID
	page_info.question_info.id = sessionStorage.getItem("question_id");


	//Prepare object to be sent with POST request
	var data = {
		username: sessionStorage.getItem("username"),
		question_id: sessionStorage.getItem("question_id")
	}

	post("/load_thread", data, function(response){


		//Render all HTML related to the current question
		var question_html = '';
		question_html += '<div id = "question_container"><div id = "vote_and_summary_container">';
		question_html += '<div class = "vote_container"><div id = "question_vote_count">';
		question_html += response.question[0][3] + '</div>';
		question_html += '<div class = "vote_buttons_container">';
		question_html += '<input type = "button" class = "vote_button" value = "Upvote">';
		question_html += '<input type = "button" class = "vote_button" value = "Downvote">';
		question_html += '</div></div><div id = "question_summary">';
		question_html += response.question[0][1] + '</div></div>';
		question_html += '<div id = "question_description_container"><div id = "question_description">';
		question_html += response.question[0][2] + '</div></div></div>';

		document.body.innerHTML += question_html;


		//Render all HTML related to the comments under the current question
		for(let i = 0; i < response.comments.length; i++){
			var comment_html = '';
			comment_html += '<div class = "comment_container" id = "';
			comment_html += response.comments[i][0] + '"><div class = "vote_container">';
			comment_html += '<div class = "vote_count_container">'
			comment_html += response.comments[i][2] + '</div><div class = "vote_buttons_container">';
			comment_html += '<input type = "button" class = "vote_button" value = "Upvote" onclick = "vote(1)">';
			comment_html += '<input type = "button" class = "vote_button" value = "Downvote" onclick = "vote(-1)">';
			comment_html += '</div></div><div class = "comment_text_container">'
			comment_html += response.comments[i][1] + '</div></div>';
			document.body.innerHTML += comment_html;
		}





		/********************************************************************************
		We need to track the current user's voting history for the current question,
		as well as each comment under the current question. This needs to be done
		in order to prevent the user from voting on the same question/comment more
		than once, unless they're trying to change their vote (from + to - or vice versa)
		********************************************************************************/

		//Check if user has previously voted on the question
		if(response.user_question_vote.length == 0){

			//If not, set vote value to zero
			page_info.question_info.user_vote = 0;
		}

		//User HAD previously voted on this question
		else{
			//Save user's vote direction
			page_info.question_info.user_vote = response.user_question_vote[0][0];
		}


		/*	For each comment under the current question:
				1. Store the comment ID
				2. Store the user's vote for that comment 	*/
		for(let i = 0; i < response.comments.length; i++){

			/*	User may not have voted on a comment, in which case there simply
				won't be a corresponding entry in the user_comment_votes array.
				That means that we have to check if there is an element
				in user_comment_votes whose first element (comment id) matches
				the id of the comment we're currently checking */

			var found_a_vote = false;

			//Iterate through user_comment_votes
			for(let j = 0; j < response.user_comment_votes.length; j++){

				//	If there's an entry matching the current comment id,
				//	add that to page_info.comment_info
				if(response.user_comment_votes[j][0] == response.comments[i][0]){
					page_info.comment_info.push({
						id: response.comments[i][0],
						vote_direction: response.user_comment_votes[j][1]
					});
					found_a_vote = true;
					break;
				}
			}

			// If there's no entry for the current comment id,
			// show that user hasn't voted on that comment
			if(found_a_vote == false){
				page_info.comment_info.push({
					id: response.comments[i][0],
					vote_direction: 0
				});
			}
		}
	});
});


var vote = function(vote_direction){

	//Find comment_id of the comment that the user voted on
	var comment_id = event.target.parentNode.parentNode.parentNode.id;

	//Check if the user had already voted in the SAME DIRECTION as the attempted vote
	var prev_vote;

	for(let i = 0; i < page_info.comment_info.length; i++){
		if(page_info.comment_info[i].id == comment_id){
			prev_vote = page_info.comment_info[i].vote_direction;
			break;
		}
	}

	//if(prev_vote == 0){

		//Update vote count in HTML
		var comment_container = document.getElementById(comment_id);
		var vote_container = comment_container.getElementsByClassName("vote_container")[0];
		var vote_count_container = vote_container.getElementsByClassName("vote_count_container")[0];
		console.log(vote_count_container.innerHTML);
		//console.log(getElementsByClassName('vote_container')[0].getElementsByClassName('vote_count_container')[0]);
		//console.log(vote_count_container.value);
		//Update page_info
		//Insert new vote into database
	//}
	//else if(prev_vote != vote_direction){
		//Update vote count in HTML
		//Update page_info
		//Update vote in database
	//}
	//console.log(prev_vote);
}


var search = function() {

	var data = {
		search_value: document.getElementById("search_bar").value
	}

	post("/search", data, function(response){
			console.log(response)
	})
}
