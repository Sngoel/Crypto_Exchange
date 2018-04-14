import psycopg2
from passlib.hash import sha256_crypt
import random
import string
import os


def check_login(login_info):

    #Define connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    sql = "SELECT * FROM users WHERE username = '" + login_info['username']
    sql += "' AND password = '" + login_info['password'] + "'"

    cur.execute(sql)
    select_result = cur.fetchall()

    print(select_result)

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

    if len(select_result) == 0:
        return False

    else:
        return True
        
"""def fuckyapasswordup():
    password9 = "treestastebad"
    letters = string.ascii_lowercase
    rand_letters = random.choices(letters,k=5)
    print(rand_letters)
    #allchar = os.urandom(8)
    salted = (password9.join(rand_letters))
    print(password9, " ", salted)
    hashed = hash(salted)
    print(hashed)


if __name__ == '__main__':
    fuckyapasswordup()"""
