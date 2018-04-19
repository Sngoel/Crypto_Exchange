import psycopg2
import sys

def submit_question(question_info):

    #Extract parameters from request object
    username = question_info['username']
    question_summary = question_info['question_summary']
    question_description = question_info['question_description']
    category = question_info['category']

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + username + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]


    insert = """ INSERT INTO questions (user_id, question_summary, question_desc, category) 
                 VALUES ('""" + str(user_id) + "', '" + question_summary + "', '" + question_description+ "', '" + str(category) + "')"

    cur.execute(insert)

    cur.close()
    conn.commit()
    conn.close()

    return "true"

def submit_comment(comment_info):

    #Extract parameters from request object
    username = comment_info['username']
    question_id = comment_info['question_id']
    comment_text = comment_info['comment_text']

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + username + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]


    insert = """ INSERT INTO comments (user_id, question_id, comment_text) 
                 VALUES ('""" + str(user_id) + "', '" + str(question_id) + "', '" + comment_text+ "')"

    cur.execute(insert)

    cur.close()
    conn.commit()
    conn.close()

    return "true"


def insert_into_users(forms):

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    
    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()


    username = forms['username']
    password = forms['password']
    email = forms['email']


    cur.execute("INSERT INTO users (username, password, email) VALUES(%s, %s, %s);" ,(username, password ,email))

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    return True


def insert_into_orders(order_info):

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()
    coin_id_in = 'LTC'
    coin_id_out = 'ETH'
    user_id = 'test'
    amount_in = order_info['amount']
    amount_out = order_info['price']

    if order_info['order_type'] == 'Buy':
        order_type = 'Buy'
    elif order_info['order_type'] == 'Sell':
        order_type = 'Sell'



    #user_id

    cur.execute("INSERT INTO open_orders (coin_id_out, coin_id_in, order_type, amount_out, amount_in) VALUES( %s, %s,%s, %s, %s);", (coin_id_out, coin_id_in, order_type, amount_out, amount_in))

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()



def insert_comment_vote(vote_info):

    username = vote_info['username']
    comment_id = vote_info['comment_id']
    vote_direction = vote_info['vote_direction']


    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + str(vote_info['username']) + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]


    insert = "INSERT INTO comment_votes (user_id, comment_id, vote_direction) VALUES (" + str(user_id) + ", " + str(comment_id) + ", " + str(vote_direction) + ")"

    cur.execute(insert)

    cur.close()
    conn.commit()
    conn.close()

    return "true"


def update_comment_vote(vote_info):

    username = vote_info['username']
    comment_id = vote_info['comment_id']
    vote_direction = vote_info['vote_direction']


    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + str(vote_info['username']) + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]

    update = "UPDATE comment_votes SET vote_direction = " + str(vote_direction) + " WHERE comment_id = " + str(comment_id) + " AND user_id = " + str(user_id)

    cur.execute(update)

    cur.close()
    conn.commit()
    conn.close()

    return "true"