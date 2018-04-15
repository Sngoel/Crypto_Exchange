

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



var clicked_search_bar = function(){

    var search_bar = document.getElementById("search_bar");
    
    if(search_bar.value == "Search"){
        search_bar.value = "";
    }
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