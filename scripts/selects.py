import psycopg2
from flask import jsonify



def get_questions():
	#Define our connection parameters
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

    return jsonify(select_result)


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
