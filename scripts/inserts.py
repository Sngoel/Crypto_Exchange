import psycopg2
import sys

coins = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'EOS', 'ADA', 'XLM', 'NEO', 'XMR']

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

    #Get question_id to return to client
    get_question_id = """ SELECT question_id 
                         FROM questions
                         WHERE user_id = '""" + str(user_id) + """' AND 
                               question_summary = '""" + question_summary + """' AND
                               question_desc = '""" + question_description + "'"

    cur.execute(get_question_id)

    question_id = cur.fetchall()[0][0]

    cur.close()
    conn.commit()
    conn.close()

    return question_id

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

    #Get comment_id to return to client
    get_comment_id = """ SELECT comment_id 
                         FROM comments
                         WHERE user_id = '""" + str(user_id) + """' AND 
                               comment_text = '""" + comment_text + "'"

    cur.execute(get_comment_id)

    comment_id = cur.fetchall()[0][0]

    cur.close()
    conn.commit()
    conn.close()

    return comment_id


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


    cur.execute("INSERT INTO users (username, password, email) VALUES(%s, %s, %s);", (username, password, email))
    cur.execute("SELECT user_id FROM users WHERE username = '" + username + "'")
    user_id = cur.fetchall()[0][0]


    #Create balances for each coin for the new user
    insert_balances = []

    for coin in coins:
        insert_balances.append("INSERT INTO balances VALUES (" + str(user_id) + ", '" + coin + "', 100)")

    for insert_balance in insert_balances:
        cur.execute(insert_balance)

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


def delete_question(question_info):


    question_id = question_info['question_id']

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    deletes = [
        "DELETE FROM question_votes WHERE question_id = " + str(question_id),
        """DELETE FROM comment_votes WHERE comment_id IN (
                SELECT comment_id FROM comments WHERE question_id = """ + str(question_id) + ")",
        "DELETE FROM comments WHERE question_id = " + str(question_id),
        "DELETE FROM questions WHERE question_id = " + str(question_id)
    ]

    for delete in deletes:
        cur.execute(delete)

    cur.close()
    conn.commit()
    conn.close()

    return "true"

def delete_comment(comment_info):

    comment_id = comment_info['comment_id']

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    deletes = [
        "DELETE FROM comment_votes WHERE comment_id = " + str(comment_id),
        "DELETE FROM comments WHERE comment_id = " + str(comment_id)
    ]

    for delete in deletes:
        cur.execute(delete)

    cur.close()
    conn.commit()
    conn.close()

    return "true"



def insert_question_vote(question_info):

    username = question_info['username']
    question_id = question_info['question_id']
    vote_direction = question_info['vote_direction']


    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + str(question_info['username']) + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]


    insert = "INSERT INTO question_votes (user_id, question_id, vote_direction) VALUES (" + str(user_id) + ", " + str(question_id) + ", " + str(vote_direction) + ")"

    cur.execute(insert)

    cur.close()
    conn.commit()
    conn.close()

    return "true"


def update_question_vote(question_info):

    username = question_info['username']
    question_id = question_info['question_id']
    vote_direction = question_info['vote_direction']


    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    #Get user_id
    get_user_id = "SELECT user_id FROM users WHERE username = '" + str(username) + "'"

    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]

    update = "UPDATE question_votes SET vote_direction = " + str(vote_direction) + " WHERE question_id = " + str(question_id) + " AND user_id = " + str(user_id)

    cur.execute(update)

    cur.close()
    conn.commit()
    conn.close()

    return "true"


def submit_order(order_info):

    ###################
    #Extract parameters
    ###################
    username = order_info['username']
    order_type = order_info['order_type']
    coin_type = order_info['coin_type']
    order_amount = float(order_info['order_amount'])
    order_price = float(order_info['order_price'])


    ##################
    #Set up connection
    ##################
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()


    ##########################
    #Get user_id from username
    ##########################
    get_user_id = "SELECT user_id FROM users WHERE username = '" + username + "'"
    cur.execute(get_user_id)
    user_id = cur.fetchall()[0][0]


    ##############################################################
    #Check the user's balance to ensure they have sufficient funds
    ##############################################################
    if order_type == "Buy":
        get_user_balance = "SELECT coin_balance FROM balances WHERE user_id = '" + str(user_id) + "' AND coin_id = 'BTC'"

    elif order_type == "Sell":
        get_user_balance = "SELECT coin_balance FROM balances WHERE user_id = '" + str(user_id) + "' AND coin_id = '" + coin_type + "'"

    cur.execute(get_user_balance)
    balance = cur.fetchall()[0][0]
  

    ################################
    #The user has insufficient funds
    ################################
    if balance < float(order_amount) / float(order_price):

        cur.close()
        conn.commit()
        conn.close()
        return "insufficient funds"



    ###########################################
    #Sufficient funds; proceed with transaction
    ###########################################
    else:

        #############################################################
        #Update user's balance by subtracting whatever they're paying
        #############################################################
        if order_type == "Buy":
            update_balance(cur, user_id, "BTC", -1 * (float(order_amount) / float(order_price)))

        elif order_type == "Sell":
            update_balance(cur, user_id, coin_type, -1 * float(order_amount))


        #########################################################
        #Find all orders in open_orders matching the user's order 
        #########################################################
        opposite_order_type = "Sell" if order_type == "Buy" else "Buy"

        cur.execute(""" SELECT order_id, user_id, amount 
                        FROM open_orders 
                        WHERE coin_id = '""" + coin_type + """' AND
                              price = '""" + str(order_price) + """' AND
                              order_type  = '""" + opposite_order_type + """' 
                        ORDER BY ts ASC """)

        result_set = cur.fetchall()


        ###################################
        #Store results in a coherent format
        ###################################
        matching_orders = []
        for matching_order in result_set:
            matching_orders.append({
                'order_id': matching_order[0],
                'user_id': matching_order[1],
                'amount': float(matching_order[2])
            })


        if len(matching_orders) == 0:

            ########################################################################
            #There are no matching orders; insert into entire order into open_orders
            ########################################################################
            cur.execute(""" INSERT INTO open_orders (user_id, order_type, coin_id, amount, price, ts) 
                            VALUES ('""" + str(user_id) + "', '" + order_type + "', '" + coin_type + "', " + str(order_amount) + ", " + str(order_price) + ", NOW())")


        else:

            ######################################################################
            #Iterate through matching orders, matching as many of them as possible
            ######################################################################
            amount_remaining = order_amount

            for matching_order in matching_orders:

                if amount_remaining > matching_order['amount']:
                    
                    #Remove the matching order from open_orders
                    delete_open_order(cur, matching_order['order_id'])

                    #Create a successful order for the current matching_order
                    create_successful_order(cur, matching_order['user_id'], user_id, opposite_order_type, coin_type, matching_order['amount'], order_price)

                    #Update both users' balances
                    if order_type == "Buy":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, coin_type, matching_order['amount'])

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], "BTC", matching_order['amount'] / order_price)

                    elif order_type == "Sell":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, "BTC", matching_order['amount'] / order_price)

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], coin_type, matching_order['amount'])
                    
                    #Update amount_remaining
                    amount_remaining -= matching_order['amount']



                elif amount_remaining < matching_order['amount']:

                    #Update matching order with new amount
                    update_open_order(cur, matching_order['order_id'], matching_order['amount'] - amount_remaining)

                    #Create a successful order for the transaction
                    create_successful_order(cur, matching_order['user_id'], user_id, opposite_order_type, coin_type, amount_remaining, order_price)
         
                    #Update both users' balances
                    if order_type == "Buy":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, coin_type, amount_remaining)

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], "BTC", amount_remaining / order_price)

                    elif order_type == "Sell":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, "BTC", amount_remaining / order_price)

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], coin_type, amount_remaining)

                    #amount_remaining should become zero
                    amount_remaining = 0
                    break


                elif amount_remaining == matching_order['amount']:

                    #Remove matching order from open_orders
                    delete_open_order(cur, matching_order['order_id'])

                    #Create a successful order for the transaction
                    create_successful_order(cur, matching_order['user_id'], user_id, opposite_order_type, coin_type, amount_remaining, order_price)

                    #Update both users' balances
                    if order_type == "Buy":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, coin_type, amount_remaining)

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], "BTC", amount_remaining / order_price)


                    elif order_type == "Sell":

                        #Update fulfiller's balance
                        update_balance(cur, user_id, "BTC", amount_remaining / order_price)

                        #Update maker's balance
                        update_balance(cur, matching_order['user_id'], coin_type, amount_remaining)

                    #amount_remaining should become zero
                    amount_remaining -= matching_order['amount']
                    break


            ################
            #End of for loop
            ################


            ####################################################################################
            #If there's still something left in amount_remaining, create a new row in open_order
            #################################################################################### 
            if amount_remaining != 0:

                cur.execute(""" INSERT INTO open_orders (user_id, order_type, coin_id, amount, price, ts) 
                                VALUES ('""" + str(user_id) + "', '" + order_type + "', '" + coin_type + "', " + str(amount_remaining) + ", " + str(order_price) + ", NOW())")

                cur.close()
                conn.commit()
                conn.close()
                return "order added"


            ################################
            #Order was completely matched up
            ################################
            elif amount_remaining == 0:

                cur.close()
                conn.commit()
                conn.close()
                return "order completed"


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()
    return 'true'



def update_balance(cur, user_id, coin_id, balance_increment):

    cur.execute(""" UPDATE balances 
                    SET coin_balance = coin_balance + """ + str(balance_increment) + """ 
                    WHERE user_id = '""" + str(user_id) + """' AND 
                          coin_id = '""" + coin_id + "'")



#Remove a row from the open_orders table
def delete_open_order(cur, order_id):

    cur.execute("DELETE FROM open_orders WHERE order_id = '" + str(order_id) + "'")



#Add a row to the successful_orders table
def create_successful_order(cur, maker_id, fulfiller_id, order_type, coin_id, amount, price):

    cur.execute(""" INSERT INTO successful_orders (maker_user_id, fulfiller_user_id, order_type , coin_id, amount, price, ts) 
        VALUES ('""" + str(maker_id) + "', '" + str(fulfiller_id) + "','" + order_type + "','""" 
                     + coin_id + "','" + str(amount) + "','" + str(price) + "', NOW())")



def update_open_order(cur, order_id, new_amount):

    cur.execute(""" UPDATE open_orders 
                    SET amount = """ + str(new_amount) + """
                    WHERE order_id = """ + str(order_id))
