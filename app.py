from flask import Flask, render_template, flash, request, redirect, url_for, logging, jsonify, json
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from simplejson import dumps as simpledumps

import sys
sys.path.insert(0, './scripts')

import login_functions
import selects
import inserts




app = Flask(__name__, static_url_path='/static')



@app.route('/')
def index():
	return render_template('landing.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/forum')
def forum():
	return render_template('forum.html')


@app.route('/thread')
def thread():
	return render_template('thread.html')






##########################################
###      POST/GET REQUEST HANDLERS     ###
##########################################


@app.route('/validate_login', methods = ['POST'])
def validate_login():
	if login_functions.check_login(request.get_json()):
		return url_for("dashboard")
	else: 
		return "false"


@app.route('/get_orders', methods = ['GET'])
def get_orders():
	return simpledumps(selects.find_orders())



#### NEED TO CHECK AND MAKE SURE THIS WAS ACTUALLY SUCCESSFUL ###
@app.route('/submit_order', methods = ['POST'])
def submit_order():
    inserts.insert_into_orders(request.get_json())
    return 'True'


@app.route('/get_questions', methods = ['POST'])
def get_questions():
	return selects.get_questions()


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=4, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=8, max=60)])
	password = StringField('Password', [validators.DataRequired(),
		validators.EqualTo('confirm', message= 'Passwords do not match')
		])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods= ['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = str(form.password.data)#sha256_crypt.encrypt(str(form.password.data))

		#Place DB Writing Stuff Here
		###
		###
		###
		#############################
		print(name,email,username,password)
		input_form = [name , email , username , str(form.password.data)]
		print("Test")
		print(input_form)
		flash('You are now registered with 0x431 Exchange')
		inserts.insert_into_users(input_form)
		return render_template('register.html', form= form)

	return render_template('register.html', form= form)



if __name__ == '__main__':
	app.secret_key = "1234"
	app.run(debug=True, threaded=True)