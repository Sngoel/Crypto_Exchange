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
    SELECT_result = cur.fetchall()

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return SELECT_result


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



    #Get id, summary description, and vote total for specified question
    get_question_info = """SELECT Q.question_id, Q.question_summary, Q.question_desc, summed.sum
                            FROM questions Q, (
                                SELECT join1.qid, sum(vote_dir)
                                FROM (
                                    SELECT Q.question_id AS qid, Q.question_summary AS q_summ, V.vote_direction AS vote_dir
                                    FROM questions Q, question_votes V WHERE Q.question_id = V.question_id) AS join1
                                GROUP BY join1.qid) AS summed
                            WHERE Q.question_id = summed.qid AND
                                  Q.question_id = '""" + question_id + "'"""



    cur.execute(get_question_info)
    thread_info['question'] = cur.fetchall()



    #Get direction of user's vote for specified question
    get_user_question_vote = """ SELECT question_votes.vote_direction
                                 FROM question_votes, users
                                 WHERE question_votes.user_id = users.user_id
                                       AND question_votes.question_id = '""" + question_id + """'
                                       AND users.username = '""" + username + "'"""

    cur.execute(get_user_question_vote)
    thread_info['user_question_vote'] = cur.fetchall()



    #Get all comments for specified question
    get_comments = """  SELECT C.comment_id, C.comment_text, summed.sum
                        FROM comments C, (
                            SELECT join1.cid, sum(join1.vote_dir)
                            FROM (
                                SELECT C.comment_id AS cid, V.vote_direction AS vote_dir
                                FROM comments C, comment_votes V
                                WHERE C.comment_id = V.comment_id) AS join1
                            GROUP BY join1.cid) AS summed
                        WHERE C.comment_id = summed.cid AND
                              C.question_id = '""" + question_id + "'"""

    cur.execute(get_comments)
    thread_info['comments'] = cur.fetchall()




    #Get direction of user's vote for each comment
    get_user_comment_votes = """ SELECT comment_votes.comment_id, comment_votes.vote_direction
                                 FROM comment_votes, users, comments
                                 WHERE comment_votes.user_id = users.user_id
                                       AND comment_votes.comment_id = comments.comment_id
                                       AND comments.question_id = '""" + question_id + """'
                                       AND users.username = '""" + username + "'"""

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
    SELECT_result = cur.fetchall()

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return SELECT_result



def search(search_info):

    input = search_info['search_text']

    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()
    questionsearch = "SELECT * FROM questions WHERE question_summary LIKE '%" + input + "%' OR question_desc LIKE '%" + input + "%' "
    cur.execute(questionsearch)
    rows = cur.fetchall()
    print(rows)

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()



    return jsonify(rows)
