import psycopg2
from flask import jsonify



def searches(input):

    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()
    questionsearch = "SELECT * FROM questions WHERE question_summary LIKE '%" + input + "%' OR question_desc LIKE '%" + input + "%'"
    cur.execute(questionsearch)
    rows = cur.fetchall()
    print(rows)

    #commentsearch = (
    #"""
    #SELECT * FROM comments c, questions q WHERE comment_text LIKE %input% AND c.question_id = q.question_id
    #"""
    #)




    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()



    return questionsearch

searches("shit")
