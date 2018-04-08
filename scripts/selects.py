import psycopg2
from flask import jsonify



def get_questions():
	#Define connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    
    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    sql = ("SELECT * FROM questions")

    cur.execute(sql)
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



    #Get summary and description for specified question
    get_question = """ SELECT * 
                       FROM questions 
                       WHERE question_id = '""" + question_id + "'"

    cur.execute(get_question)
    thread_info['question_info'] = cur.fetchall()



    #Get total vote count for specified question
    get_question_votes = """ SELECT SUM(vote_direction) 
                             FROM question_votes 
                             WHERE question_id = '""" + question_id + "'"

    cur.execute(get_question_votes)
    thread_info['question_vote_count'] = cur.fetchall()



    #Get direction of user's vote for specified question                         
    get_user_question_vote = """ SELECT question_votes.vote_direction 
                                 FROM question_votes, users
                                 WHERE question_votes.user_id = users.user_id
                                       AND question_votes.question_id = '""" + question_id + """' 
                                       AND users.username = '""" + username + "'"

    cur.execute(get_user_question_vote)
    thread_info['user_question_vote'] = cur.fetchall()
    


    #Get all comments for specified question
    get_comments = """ SELECT * 
                       FROM comments 
                       WHERE question_id = '""" + question_id + "'"

    cur.execute(get_comments)
    thread_info['comments'] = cur.fetchall()



    #Get total vote count for all comments
    get_comment_votes = """ SELECT comment_votes.comment_id, SUM(comment_votes.vote_direction) 
                            FROM comment_votes, comments 
                            WHERE comments.question_id = '""" + question_id + """'
                                  AND comments.comment_id = comment_votes.comment_id 
                            GROUP BY comment_votes.comment_id"""

    cur.execute(get_comment_votes)
    thread_info['comment_vote_counts'] = cur.fetchall()    



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

