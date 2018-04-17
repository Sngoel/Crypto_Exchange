import psycopg2
import sys

def insert_into_users(forms):

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    name = forms[0]
    email = forms[1]
    username = forms[2]
    password = forms[3]


    cur.execute("INSERT INTO users (username, password, email) VALUES(%s, %s, %s);" ,(username, password ,email))

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()


def insert_into_orders(order_info):

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    amount = order_info['amount']

    if order_info['order_type'] == 'Buy':
        order_type = 'Buy'
    elif order_info['order_type'] == 'Sell':
        order_type = 'Sell'

        #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + str(order_info['username']) + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]

    #user_id

    cur.execute("INSERT INTO open_orders (user_id, coin_id, order_type ,amount, order_time) VALUES( %s, %s, %s, %s, %s);", (user_id, coin_id, order_type ,amount, order_time))

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()



def insert_questions(questioninfo):
    #Define our connection string
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    print("Hello World!")
    # print the connection string we will use to connect
    #print "Connecting to database\n    ->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cur = conn.cursor()
    user_id = questioninfo[0]
    question_summary = questioninfo[1]
    question_desc = questioninfo[2]
    category = questioninfo[3]


    cur.execute("""INSERT INTO questions(user_id, question_summary, question_desc, category) VALUES(%s, %s, %s, %s);""" ,(user_id, question_summary, question_desc ,category))

    cur.close()
    conn.commit()
    conn.close()
