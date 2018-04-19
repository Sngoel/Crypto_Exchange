var page_info = {
	question_info: {
		id: undefined,
		user_vote: undefined
	},
	comment_info: []
}


$(document).ready(function(){

	//If user is not currently logged in, redirect to landing page
	check_if_logged_in();

	//Save off question ID
	page_info.question_info.id = sessionStorage.getItem("question_id");

	//Prepare POST request data object
	var data = {
		username: sessionStorage.getItem("username"),
		question_id: sessionStorage.getItem("question_id")
	}

	post("/load_thread", data, function(response){

		console.log(response);

		//Render all HTML related to the current question
		var question_html = '';

		question_html += '<div class="well well-sm"><div style = "width: 15%; display: inline-block">';
		question_html += '<div class = "vote_count_container">' + response.question_vote_count[0] + '</div>';
		question_html += '<div class="btn-group-vertical" style = "display: inline-block">';
		question_html += '<button type="button" class="btn btn-success">Upvote</button>';
		question_html += '<button type="button" class="btn btn-danger">Downvote</button>';
		question_html += '</div></div><div id = "question_text_container">';
		question_html += '<div style = "font-size: 200%;">' + response.question[2] + '</div>';
		question_html += '<div style = "font-size: 100%;">' + response.question[3] + '</div>';
		question_html += '</div></div>';

		document.body.innerHTML += question_html;


		//Render all HTML related to the comments under the current question
		for(let i = 0; i < response.comments.length; i++){
			var comment_html = '';
			comment_html += '<div class="well well-sm" id = "' + response.comments[i][0] + '">';
			comment_html += '<div style = "width: 15%; display: inline-block;">';
			comment_html += '<div class = "vote_count_container">' + response.comment_votes[i][1] + '</div>';
			comment_html += '<div class="btn-group-vertical" style = "display: inline-block;">';
			comment_html += '<button type="button" class="btn btn-success" onclick = "comment_vote(1)">Upvote</button>';
			comment_html += '<button type="button" class="btn btn-danger" onclick = "comment_vote(-1)">Downvote</button>';
			comment_html += '</div></div>';
			comment_html += '<div class = "comment_text_container">';
			comment_html += response.comments[i][3] + '</div></div>';
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


var comment_vote = function(vote_direction){

	//Find comment_id of the comment that the user voted on
	var comment_id = event.target.parentNode.parentNode.parentNode.id;

	//Check if the user had already voted in the SAME DIRECTION as the attempted vote
	var prev_vote;
	var comment_index;

	for(let i = 0; i < page_info.comment_info.length; i++){
		if(page_info.comment_info[i].id == comment_id){
			comment_index = i;
			prev_vote = page_info.comment_info[i].vote_direction;
			break;
		}
	}


	if(prev_vote == 0){

		//Update vote count in HTML
		var vote_count_container = document.getElementById(comment_id).children[0].children[0];
		var current_vote = parseInt(vote_count_container.innerHTML);
		vote_count_container.innerHTML = current_vote + vote_direction;
		
		//Update page_info
		page_info.comment_info[comment_index].vote_direction = vote_direction;

		//Set up post request data object
		var data = {
			username: sessionStorage.getItem("username"),
			comment_id: comment_id,
			vote_direction: vote_direction
		};

		//Send request to server
		post("/insert_comment_vote", data, function(response){
			console.log(response);
		});

	}

	else if(prev_vote != vote_direction){

		//Update vote count in HTML
		var vote_count_container = document.getElementById(comment_id).children[0].children[0];
		var current_vote = parseInt(vote_count_container.innerHTML);
		vote_count_container.innerHTML = current_vote + 2 * vote_direction;

		//Update page_info
		page_info.comment_info[comment_index].vote_direction = vote_direction;

		//Set up post request data object
		var data = {
			username: sessionStorage.getItem("username"),
			comment_id: comment_id,
			vote_direction: vote_direction
		};

		//Send request to server
		post("/update_comment_vote", data, function(response){
			console.log(response);
		});
	}
}