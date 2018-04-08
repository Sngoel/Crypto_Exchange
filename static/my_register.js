var submit = function(){

	//Check if any fields are empty
	var fields = ["name", "email", "username", "password", "confirm_password"];

	for(let i = 0; i < fields.length; i++){
		if(document.getElementById(fields[i]).value === ""){
			alert("Please fill out all fields");
			return;
		}
	}

	//Check if email is valid
	if(!email_is_ok(document.getElementById("email").value)){
		alert("Invalid email");
		return;
	}

	//Check if passwords match
	if(document.getElementById("password").value !== document.getElementById("confirm_password").value){
		alert("Password does not match");
		return;
	}


	var registration_data = {
		name: document.getElementById("name").value,
		email: document.getElementById("email").value,
		username: document.getElementById("username").value,
		password: document.getElementById("password").value,
	}

	post("/register", registration_data, function(response){
		console.log(response);
	});

	/*//Send 
	$.post("/register", json = registration_data, function(response){
		console.log(response);
	});*/
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