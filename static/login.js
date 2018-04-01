
var validate = function(){

	username = document.getElementById("username").value;
	password = document.getElementById("password").value;

	if(username === "" || password === ""){
		alert("Please fill out all fields");
	}

	var login_info = {
		username: username,
		password: password
	};

	post("/validate_login", login_info, function(response){
		if(response === "false"){
			alert("Invalid username / password combination");
		}
		else{
			sessionStorage.setItem("username", username);
			window.location = response;
		}
	});
}





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