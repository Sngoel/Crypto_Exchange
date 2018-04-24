import psycopg2
from flask import jsonify



def get_questions():

	#Define connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    #Initialize array of questions
    questions = []

    #Get all questions
    get_questions =  "SELECT question_id, question_summary FROM questions"

    cur.execute(get_questions)
    result_set = cur.fetchall()

    for question in result_set:
        questions.append({
                'question_id': question[0],
                'question_summary': question[1]
            })

    #Get vote totals for all questions
    get_question_votes = """ SELECT question_id, COALESCE(SUM(vote_direction), 0)
                             FROM question_votes
                             GROUP BY question_id """

    cur.execute(get_question_votes)
    result_set = cur.fetchall()

    for question in questions:
        found = False

        for question_vote in result_set:
            if question['question_id'] == question_vote[0]:
                found = True
                question['vote_count'] = question_vote[1]
                break

        if found == False:
            question['vote_count'] = 0


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return questions



def search(search_info):

    search_text = search_info['search_text']

    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    questions = []

    search_query = """ SELECT question_id, question_summary
                       FROM questions
                       WHERE question_summary LIKE '%""" + search_text + """%' OR 
                             question_desc LIKE '%""" + search_text + "%'"

    cur.execute(search_query)
    result_set = cur.fetchall()

    for question in result_set:
        questions.append({
            'question_id': question[0],
            'question_summary': question[1]
            })

    #Get question votes
    get_question_votes = """ SELECT question_id, COALESCE(SUM(vote_direction), 0)
                             FROM question_votes
                             WHERE question_id IN (
                                SELECT question_id
                                FROM questions
                                WHERE question_summary LIKE '%""" + search_text + """%' OR 
                                      question_desc LIKE '%""" + search_text + """%')
                             GROUP BY question_id"""

    cur.execute(get_question_votes)
    result_set = cur.fetchall()

    for question in questions:
        found = False

        for question_vote in result_set:
            if question['question_id'] == question_vote[0]:
                found = True
                question['vote_count'] = question_vote[1]
                break

        if found == False:
            question['vote_count'] = 0


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return questions


def load_thread(request):

    #Define our connection parameters, connect to database, initialize cursor
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    #Extract parameters
    username = request['username']
    question_id = request['question_id']

    #Get user_id from username
    cur.execute("SELECT user_id FROM users WHERE username = '" + username + "'")
    user_id = cur.fetchall()[0][0]




    #Initialize dictionary for storing question information
    question_info = {
        'user_asked_question': 0
    }

    #Get all information in questions table for specified question    
    cur.execute("SELECT * FROM questions WHERE question_id = '" + question_id + "'")
    result_set = cur.fetchall()[0]

    question_info['question_id'] = result_set[0]
    question_info['question_summary'] = result_set[2]
    question_info['question_description'] = result_set[3]
    question_info['question_category'] = result_set[4]

    #Indicate if user_id's match
    if result_set[1] == user_id:
        question_info['user_asked_question'] = 1


    #Get vote count associated with specified question
    get_question_vote_count = """ SELECT COALESCE(SUM(vote_direction), 0)
                                  FROM question_votes
                                  WHERE question_id = '""" + question_id + "'"

    cur.execute(get_question_vote_count)
    question_info['vote_count'] = cur.fetchall()[0][0]


    #Get direction of user's vote for specified question                         
    get_user_question_vote = """ SELECT V.vote_direction 
                                 FROM question_votes V, users U
                                 WHERE V.user_id = U.user_id
                                       AND V.question_id = '""" + question_id + """' 
                                       AND U.username = '""" + username + "'"

    cur.execute(get_user_question_vote)

    result_set = cur.fetchall()

    if len(result_set) == 0:
        question_info['user_question_vote'] = 0

    else:
        question_info['user_question_vote'] = result_set[0][0]

    





    #Initialize list for holding information about comments for the current question
    comments = []

    #Get all information from comments table for current question
    cur.execute("SELECT comment_id, user_id, comment_text FROM comments WHERE question_id = '" + question_id + "'")

    result_set = cur.fetchall()

    for comment in result_set:

        user_posted_comment = 0

        if comment[1] == user_id:
            user_posted_comment = 1

        comments.append({
            'comment_id': comment[0],
            'comment_text': comment[2],
            'user_posted_comment': user_posted_comment
        })


    #Get vote counts for each comment associated with a specific question
    get_comment_votes = """ SELECT V.comment_id, COALESCE(SUM(V.vote_direction), 0) 
                            FROM comment_votes V, comments C 
                            WHERE V.comment_id = C.comment_id AND 
                                  C.question_id = '""" + question_id + """' 
                            GROUP BY V.comment_id"""
                           
    cur.execute(get_comment_votes)
    comment_vote_counts = cur.fetchall()

    #Add vote_count attribute to comments list
    for comment in comments:
        found = False

        for comment_vote_count in comment_vote_counts:
            if comment['comment_id'] == comment_vote_count[0]:
                found = True
                comment['vote_count'] = comment_vote_count[1]
                break

        if found == False:
            comment['vote_count'] = 0


    #Get direction of user's vote for each comment                     
    get_user_comment_votes = """ SELECT V.comment_id, V.vote_direction 
                                 FROM comment_votes V, comments C
                                 WHERE V.user_id = '""" + str(user_id) + """' AND 
                                       V.comment_id = C.comment_id AND
                                       C.question_id = '""" + str(question_id) + "'"

    cur.execute(get_user_comment_votes)
    user_comment_votes = cur.fetchall()
    #Add user's vote direction as attribute to comments list
    for comment in comments:
        found = False

        for user_comment_vote in user_comment_votes:
            if comment['comment_id'] == user_comment_vote[0]:
                found = True
                comment['user_comment_vote'] = user_comment_vote[1]
                break

        if found == False:
            comment['user_comment_vote'] = 0


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    #Encapsulate all information into one dictionary
    thread_info = {
        'question_info': question_info,
        'comments': comments
    }

    return thread_info

def find_orders():
    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    sql = ("SELECT * FROM open_orders")

    cur.execute(sql)
    select_result = cur.fetchall()

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return select_result




