import psycopg2
from passlib.hash import sha256_crypt


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

