import psycopg2
import sys
from random import randint


coins = ['BTC', 'LTC', 'ETH']



def create_and_populate_tables():

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    creates = (
        """CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(20) UNIQUE,
            password VARCHAR(30),
            email VARCHAR(50) UNIQUE)""",

        """INSERT INTO users (username, password, email) VALUES
            ('alex1996', 'password1', 'asdf1@gmail.com'),
            ('alex1995', 'password2', 'asdf2@gmail.com'),
            ('alex1994', 'password3', 'asdf3@gmail.com'),
            ('alex1993', 'password4', 'asdf4@gmail.com')""",



        """CREATE TABLE open_orders(
                order_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                coin_id_out VARCHAR(3),
                coin_id_in VARCHAR(3),
                order_type VARCHAR(4),
                amount_out DECIMAL(12,8),
                amount_in DECIMAL(12,8))""",

        "INSERT INTO open_orders (user_id, coin_id_out, coin_id_in, order_type, amount_out, amount_in) VALUES " + generate_orders(1000, 4, ["LTC", "BTC", "ETH", "DGC", "TDE", "IST"]),

        """CREATE TABLE coins(
                coin_id varchar(3)
        )""",

        """INSERT INTO coins (coin_id) VALUES
            ('BTC'),
            ('ETH'),
            ('XRP'),
            ('BCH'),
            ('LTC'),
            ('EOS'),
            ('ADA'),
            ('XLM'),
            ('NEO'),
            ('XMR')
            """,



        """CREATE TABLE questions (
                question_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                question_summary VARCHAR(255) NOT NULL,
                question_desc VARCHAR(1000),
                category VARCHAR(30))""",

        """INSERT INTO questions (user_id, question_summary, question_desc, category) VALUES
            (3, 'This is the first question in the database', 'This is the description for the first question', 'Memes'),
            (3, 'We added this question after the first', 'Description number 2', 'Memes'),
            (2, 'We figured four questions would be enough for testing purposes', 'This is the third description', 'Memes'),
            (1, 'This is our last question, but we will add more later', 'You can take this description to the bank', 'Memes')
            """,



        """CREATE TABLE comments (
                comment_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                question_id INT REFERENCES questions(question_id),
                comment_text VARCHAR(1000) NOT NULL)""",

        """INSERT INTO comments (user_id, question_id, comment_text) VALUES
            (4, 1, 'This comment, and all the ones following it, are for the first question'),
            (2, 1, 'This is the second comment'),
            (1, 1, 'All of these comments have the question_id as the foreign key'),
            (3, 1, 'We also track which user made this comment, so only that user can delete this comment'),
            (3, 1, 'Eventually, we will make it so that users can upvote and downvote comments AND questions')
        """,

        """CREATE TABLE question_votes(
            user_id INT REFERENCES users(user_id),
            question_id INT REFERENCES questions(question_id),
            vote_direction INT,
            UNIQUE(user_id, question_id))""",



        """CREATE TABLE comment_votes(
            user_id INT REFERENCES users(user_id),
            comment_id INT REFERENCES comments(comment_id),
            vote_direction INT,
            UNIQUE(user_id, comment_id))""",


        """CREATE TABLE categories(
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR[30],
                parent_category INT REFERENCES categories(category_id))""")





#user_id in will have to go back into open_orders
    selects = (
        "SELECT * FROM users",
        "SELECT * FROM questions",
        "SELECT * FROM comments",
        "SELECT * FROM open_orders"
    )


    for create in creates:
        cur.execute(create)

    for select in selects:
        cur.execute(select)
        rows = cur.fetchall()
        for row in rows:
            print(row)


    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()


#This function generates an SQL-formatted string of random 
# buy/sell orders, which is used to populate the order table
def generate_orders(number_of_entries, number_of_users, coins):

    order_strings = ""
    order_types = ["Buy", "Sell"]

    for i in range(0, number_of_entries):

        user_id = randint(1, number_of_users)
        coin1 = coins[randint(0, len(coins) - 1)]
        coin2 = coins[randint(0, len(coins) - 1)]

        #Make sure the two coins are different
        while coin2 == coin1:
            coin2 = coins[randint(0, len(coins) - 1)]

        order_type = order_types[randint(0, 1)]
        amount1 = randint(1, 100)
        amount2 = randint(1, 100)


        if i == 0:
            order_strings += "(" + str(user_id) + ", '" + coin1 + "', '" + coin2 + "', '" + order_type + "', " + str(amount1) + ", " + str(amount2) + ")"

        else:
            order_strings += ",\n(" + str(user_id) + ", '" + coin1 + "', '" + coin2 + "', '" + order_type + "', " + str(amount1) + ", " + str(amount2) + ")"

    return order_strings


create_and_populate_tables()