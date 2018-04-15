var register_toggled = true;

var toggle = function(){

	//Toggle to login form; hide email and password fields
	if(register_toggled){

		//Save current state
		register_toggled = false;

		//Make the toggle button say "Create an Account"
		document.getElementById("toggle").value = "Create an Account"

		//Make the submit button say "Log In"
		document.getElementById("submit").value = "Log In"

		//Hide email field
		document.getElementById("email_p").style.display = "None";
		document.getElementById("email").style.display = "None";

		//Hide confirm password field
		document.getElementById("confirm_password_p").style.display = "None";
		document.getElementById("confirm_password").style.display = "None";
	}

	else{

		//Save current state
		register_toggled = true;

		//Make the toggle button say "Log In"
		document.getElementById("toggle").value = "Log In"

		//Make the submit button say "Register"
		document.getElementById("submit").value = "Register"

		//Restore email field
		document.getElementById("email_p").style.display = "inline";
		document.getElementById("email").style.display = "inline";

		//Restore confirm password field
		document.getElementById("confirm_password_p").style.display = "inline";
		document.getElementById("confirm_password").style.display = "inline";
	}
};


//This function will either create a new user or atttempt to authenticate the given credentials
//We use the global register_toggled variable to know which operation to attempt.
var validate = function(){

	//Collect user data from input fields
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;

	//These will only be used if the user is registering, not logging in
	var email = document.getElementById("email").value;
	var confirm_password = document.getElementById("confirm_password").value;
	


	//User is trying to register
	if (register_toggled){

		//Alert an error if any fields have been left empty
		var fields = ["email", "username", "password", "confirm_password"];

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
		post("/registration", registration_info, function(response){
			if(response === "false"){
				alert("A problem occurred during registration");
			}
			else{
				sessionStorage.setItem("username", username);
				window.location = response;
			}

		});
	}

	//User is trying to login
	else {

		//Make sure fields aren't empty
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