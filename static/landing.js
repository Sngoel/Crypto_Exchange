var register_toggled = true;

var login = function(){

	//Save current state
	register_toggled = false;

	//Hide register form
	document.getElementById("register").style.display = "None";

	//Show login form
	document.getElementById("login").style.display = "inline-block";
};

var register = function(){

	//Save current state
	register_toggled = true;

	//Hide register form
	document.getElementById("login").style.display = "None";

	//Show login form
	document.getElementById("register").style.display = "inline-block";

}


//This function will either create a new user or atttempt to authenticate the given credentials
//We use the global register_toggled variable to know which operation to attempt.
var validate = function(){

	//User is trying to register
	if(register_toggled){

		//Collect user data from input fields
		var email = document.getElementById("email").value;
		var username = document.getElementById("register_username").value;
		var password = document.getElementById("register_password").value;
		var confirm_password = document.getElementById("confirm_password").value;

		//Alert an error if any fields have been left empty
		var fields = ["email", "register_username", "register_password", "confirm_password"];

		for(let i = 0; i < fields.length; i++){
			if(document.getElementById(fields[i]).value === ""){
				alert("Please fill out all fields");
				return;
			}
		}

		//Check if email is valid
		if(!email_is_ok(email)){
			alert("Invalid email");
			return;
		}

		//Check if passwords match
		if(password !== confirm_password){
			alert("Password does not match");
			return;
		}

		//Create data object for POST request
		var registration_info = {
			email: email,
			username: username,
			password: password
		}

		//POST new user info to server
		try{
		post("/registration", registration_info, function(response){
			if(response === "False"){
				alert("Username already in use");
				return;
			}
			else{
				sessionStorage.setItem("username", username);
				window.location = response;
				}
			}
		}
	}

	//User is trying to login
	else {

		//Collect user data from input fields
		var username = document.getElementById("login_username").value;
		var password = document.getElementById("login_password").value;


		//Make sure fields aren't empty

		if(username === "" || password === ""){
			alert("Please fill out all fields");
		}
			var login_info = {
				username: username,
				password: password
		}};

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

}


var email_is_ok = function(email){

	if(!email.includes("@")){
		return false;
	}

	var email_suffixes = [".com", ".net", ".edu", ".gov"];
	var email_ok = false;

	for(let i = 0; i < email_suffixes.length; i++){
		if(email.includes(email_suffixes[i])){
			email_ok = true;
			break;
		}
	}

	if(!email_ok){
		return false;
	}

	return true;
}
