import psycopg2
import hashlib
import time


def check_login(login_info):

    #Define connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()
    password = login_info['password']
    print(password)
    passwordnew = hashlib.md5(password.encode())
    print(passwordnew)
    flowit = passwordnew.hexdigest()
    print(flowit)


    sql = "SELECT * FROM users WHERE username = '" + login_info['username']
    sql += "' AND password = '" + flowit + "'"

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
