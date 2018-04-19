import psycopg2
from flask import jsonify



def get_questions():
	#Define connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    
    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    questions = """ SELECT Q.question_id, Q.question_summary, COALESCE(SUM(V.vote_direction), 0) 
                    FROM questions Q, question_votes V 
                    WHERE Q.question_id = V.question_id 
                    GROUP BY Q.question_id"""

    cur.execute(questions)
    select_result = cur.fetchall()

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return select_result


def load_thread(request):

    #Define our connection parameters, connect to database, initialize cursor
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    #Extract parameters
    username = request['username']
    question_id = request['question_id']


    #Initialize return dictionary
    thread_info = {}



    #Get all information in questions table for specified question    
    get_question_info = "SELECT * FROM questions WHERE question_id = '" + question_id + "'"

    cur.execute(get_question_info)
    thread_info['question'] = cur.fetchall()[0]



    #Get vote count associated with specified question
    get_question_vote_count = """ SELECT COALESCE(SUM(vote_direction), 0)
                                  FROM question_votes
                                  WHERE question_id = '""" + question_id + "'"

    cur.execute(get_question_vote_count)
    thread_info['question_vote_count'] = cur.fetchall()[0]



    #Get direction of user's vote for specified question                         
    get_user_question_vote = """ SELECT question_votes.vote_direction 
                                 FROM question_votes, users
                                 WHERE question_votes.user_id = users.user_id
                                       AND question_votes.question_id = '""" + question_id + """' 
                                       AND users.username = '""" + username + "'"

    cur.execute(get_user_question_vote)
    thread_info['user_question_vote'] = cur.fetchall()
    


    #Get all comments for specified question
    get_comments = "SELECT * FROM comments WHERE question_id = '" + question_id + "'"

    cur.execute(get_comments)
    thread_info['comments'] = cur.fetchall()



    #Get vote counts for each comment associated with a specific question
    get_comment_votes = """ SELECT V.comment_id, COALESCE(SUM(V.vote_direction), 0) 
                            FROM comment_votes V, comments C 
                            WHERE V.comment_id = C.comment_id AND 
                                  C.question_id = '""" + question_id + """' 
                            GROUP BY V.comment_id"""
                           
    cur.execute(get_comment_votes)
    thread_info['comment_votes'] = cur.fetchall()



    #Get direction of user's vote for each comment                     
    get_user_comment_votes = """ SELECT comment_votes.comment_id, comment_votes.vote_direction 
                                 FROM comment_votes, users, comments
                                 WHERE comment_votes.user_id = users.user_id
                                       AND comment_votes.comment_id = comments.comment_id
                                       AND comments.question_id = '""" + question_id + """' 
                                       AND users.username = '""" + username + "'"

    cur.execute(get_user_comment_votes)
    thread_info['user_comment_votes'] = cur.fetchall()


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

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


def search(search_info):

    search_text = search_info['search_text']

    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    search_query = """ SELECT Q.question_id, Q.question_summary, COALESCE(SUM(V.vote_direction), 0) 
                       FROM questions Q, question_votes V 
                       WHERE Q.question_id = V.question_id AND 
                             Q.question_summary LIKE '%""" + search_text + """%' OR 
                             Q.question_desc LIKE '%""" + search_text + """%' 
                       GROUP BY Q.question_id"""

    
    cur.execute(search_query)
    rows = cur.fetchall()
    print(rows)

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()



    return jsonify(rows)

