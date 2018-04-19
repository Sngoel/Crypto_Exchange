

//POST wrapper function
var post = function(url, data, callback){
	$.ajax({
        type : "POST",
        url : url,
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
            callback(response);
        }
    });
}


//GET wrapper function
var get = function(url, callback){
    $.ajax({
        type : "GET",
        url : url,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
        	callback(response);
        }
    });
}



var search = function(){

    //Get user's input from search bar
    var search_text = document.getElementById('search_bar').value

    //Save search text in cookie
    sessionStorage.setItem("search_text", search_text);

    //Redirect to search_results.html, which will perform the search on page load
    window.location = "/search_results";
}


var log_out = function(){

    //Remove username from cookie
    sessionStorage.removeItem("username");

    //Redirect user to landing page
    window.location = "/";
}

var check_if_logged_in = function(){

    if(sessionStorage.getItem("username") === null){
        alert("Please log in to access the 0x431 Crypto Exchange");
        window.location = "/"
    }
}