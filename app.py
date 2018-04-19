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


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/forum')
def forum():
	return render_template('forum.html')


@app.route('/thread')
def thread():
	return render_template('thread.html')


@app.route('/search_results')
def search_results():
	return render_template('search_results.html')






##########################################
###      POST/GET REQUEST HANDLERS     ###
##########################################


@app.route('/search', methods = ['POST'])
def search():
	return selects.search(request.get_json())

@app.route('/get_questions', methods = ['POST'])
def get_questions():
	return jsonify(selects.get_questions())#Need to add category parameter


@app.route('/load_thread', methods = ['POST'])
def load_thread():
	return jsonify(selects.load_thread(request.get_json()))


@app.route('/get_orders', methods = ['GET'])
def get_orders():
	return jsonify(selects.find_orders())


@app.route("/submit_question", methods = ['POST'])
def submit_question():
	return jsonify(inserts.submit_question(request.get_json()))

@app.route("/submit_comment", methods = ['POST'])
def submit_comment():
	return jsonify(inserts.submit_comment(request.get_json()))


#### NEED TO CHECK AND MAKE SURE THIS WAS ACTUALLY SUCCESSFUL ###
@app.route('/submit_order', methods = ['POST'])
def submit_order():
    inserts.insert_into_orders(request.get_json())
    return 'True'


@app.route('/registration', methods = ['POST'])
def registration():
	if inserts.insert_into_users(request.get_json()):
		return url_for("dashboard")
	else:
		return "false"


@app.route('/validate_login', methods = ['POST'])
def validate_login():
	if login_functions.check_login(request.get_json()):
		return url_for("dashboard")
	else: 
		return "false"


@app.route('/update_comment_vote', methods = ['POST'])
def update_comment_vote():
	return inserts.update_comment_vote(request.get_json())


@app.route('/insert_comment_vote', methods = ['POST'])
def insert_comment_vote():
	return inserts.insert_comment_vote(request.get_json())





if __name__ == '__main__':
	app.secret_key = "1234"
	app.run(debug=True, threaded=True)