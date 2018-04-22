
//Question, comments info will be saved here
var page_info = {};


$(document).ready(function(){

	//If user is not currently logged in, redirect to landing page
	check_if_logged_in();


	//Prepare POST request data object
	var data = {
		username: sessionStorage.getItem("username"),
		question_id: sessionStorage.getItem("question_id")
	}

	post("/load_thread", data, function(response){

		page_info = response;
		console.log(response);

		/********************************************************************************
		We need to track the current user's voting history for the current question, 
		as well as each comment under the current question. This needs to be done 
		in order to prevent the user from voting on the same question/comment more 
		than once, unless they're trying to change their vote (from + to - or vice versa)
		********************************************************************************/


		//Render all HTML related to the current question
		var question_html = '';

		question_html += '<div class="well well-sm" style = "width: 90%; margin-left: 5%;"><div style = "width: 15%; display: inline-block">';
		question_html += '<div class = "vote_count_container">' + response.question_info.vote_count + '</div>';
		question_html += '<div class="btn-group-vertical" style = "display: inline-block">';
		question_html += '<button type="button" class="btn btn-success">Upvote</button>';
		question_html += '<button type="button" class="btn btn-danger">Downvote</button>';
		question_html += '</div></div><div id = "question_text_container">';
		question_html += '<div style = "font-size: 200%;">' + response.question_info.question_summary + '</div>';
		question_html += '<div style = "font-size: 100%;">' + response.question_info.question_description + '</div>';

		if(page_info.question_info.user_asked_question){
			question_html += '<button type = "button" class = "btn btn-danger" style = "display: inline-block; float: right;" onclick = "delete_question(event)">Delete</button>';
		}
		
		question_html += '</div></div>';

		//document.body.innerHTML += question_html;
		document.getElementById("question").innerHTML += question_html;

		var comment_form = '';
		comment_form += '<div class = "well well-sm" style = "width: 90%; margin-left: 5%;">';
		comment_form += '<input type="text" style = "display: inline-block; width: 93%;" class="form-control" id = "new_comment" placeholder="Comment">';
		comment_form += '<button type="button" class="btn btn-default" style = "display: inline-block; float: right;" onclick = "submit_comment()">Submit</button>';
		comment_form += '</div>';
		//document.body.innerHTML += comment_form;
		document.getElementById("question").innerHTML += comment_form;

		//Render all HTML related to the comments under the current question
		for(let i = 0; i < page_info.comments.length; i++){
			var comment_html = '';
			comment_html += '<div class="well well-sm"  style = "width: 90%; margin-left: 5%;" id = "' + response.comments[i].comment_id + '">';
			comment_html += 	'<div style = "width: 15%; display: inline-block;">';
			comment_html += 		'<div class = "vote_count_container">' + response.comments[i].vote_count + '</div>';
			comment_html += 		'<div class="btn-group-vertical" style = "display: inline-block;">';
			comment_html += 			'<button type="button" class="btn btn-success" onclick = "comment_vote(1)">Upvote</button>';
			comment_html += 			'<button type="button" class="btn btn-danger" onclick = "comment_vote(-1)">Downvote</button>';
			comment_html += 		'</div>';
			comment_html += 	'</div>';
			comment_html += 	'<div class = "comment_text_container">' + response.comments[i].comment_text;

			if(page_info.comments[i].user_posted_comment){
				comment_html +=	'<button type = "button" class = "btn btn-danger" style = "display: inline-block; float: right;" onclick = "delete_comment(event)">Delete</button>';
			}

			
			comment_html += 	'</div>';
			comment_html += '</div>';
			//document.body.innerHTML += comment_html;
			document.getElementById("comments").innerHTML += comment_html;
		}
	});
});


var comment_vote = function(vote_direction){

	//Find comment_id of the comment that the user voted on
	var comment_id = event.target.parentNode.parentNode.parentNode.id;

	//Check if the user had already voted in the SAME DIRECTION as the attempted vote
	var prev_vote;
	var comment_index;

	for(let i = 0; i < page_info.comments.length; i++){
		if(page_info.comments[i].comment_id == comment_id){
			comment_index = i;
			prev_vote = page_info.comments[i].user_comment_vote;
			break;
		}
	}


	if(prev_vote == 0){

		//Update vote count in HTML
		var vote_count_container = document.getElementById(comment_id).children[0].children[0];
		var current_vote = parseInt(vote_count_container.innerHTML);
		vote_count_container.innerHTML = current_vote + vote_direction;
		
		//Update page_info
		page_info.comments[comment_index].user_comment_vote = vote_direction;

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
		page_info.comments[comment_index].user_comment_vote = vote_direction;

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

var submit_comment = function(){

	var data = {
		username: sessionStorage.getItem("username"),
		question_id: sessionStorage.getItem("question_id"),
		comment_text: document.getElementById("new_comment").value
	}

	post("/submit_comment", data, function(response){
		console.log(response);

		page_info.comments.push({
			comment_id: response,
			comment_text: document.getElementById("new_comment").value,
			user_comment_vote: 0,
			vote_count: 0,
			user_posted_comment: 1
		});

		var comment_html = '';
		comment_html += '<div class="well well-sm"  style = "width: 90%; margin-left: 5%;" id = "' + response + '">';
		comment_html += 	'<div style = "width: 15%; display: inline-block;">';
		comment_html += 		'<div class = "vote_count_container">0</div>';
		comment_html += 		'<div class="btn-group-vertical" style = "display: inline-block;">';
		comment_html += 			'<button type="button" class="btn btn-success" onclick = "comment_vote(1)">Upvote</button>';
		comment_html += 			'<button type="button" class="btn btn-danger" onclick = "comment_vote(-1)">Downvote</button>';
		comment_html += 		'</div>';
		comment_html += 	'</div>';
		comment_html += 	'<div class = "comment_text_container">' + document.getElementById("new_comment").value;
		comment_html +=	'<button type = "button" class = "btn btn-danger" style = "display: inline-block; float: right;" onclick = "delete_comment(event)">Delete</button>';
		comment_html += 	'</div>';
		comment_html += '</div>';

		document.getElementById("comments").innerHTML = comment_html + document.getElementById("comments").innerHTML;
		document.getElementById("new_comment").value = "";

	});
}

var delete_comment = function(event){

	//Find comment container element
	var comment_element = event.target.parentNode.parentNode;

	//Find comment_id
	var comment_id = comment_element.id;

	//Remove corresponding HTML
	comment_element.parentNode.removeChild(comment_element);

	//Remove from database
	var data = {
		comment_id: comment_id
	}

	post("/delete_comment", data, function(response){

		//Remove comment metadata from page_info.comments
		for(let i = 0; i < page_info.comments.length; i++){
			if(page_info.comments[i].comment_id == comment_id){
				page_info.comments.splice(i, 1);
				break;
			}
		}
	});

	//console.log(comment_id);
}

var delete_question = function(event){

    //Delete from database
	var data = {
		question_id: sessionStorage.getItem("question_id")
	}

	console.log(data);

	post("/delete_question", data, function(response){
		console.log(response);
	});

    //Redirect user to forum
    window.location = "/forum";
}