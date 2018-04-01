import psycopg2
import sys

def delete_tables():

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    commands = (
        "DROP TABLE users CASCADE",
        "DROP TABLE comments CASCADE",
        "DROP TABLE questions CASCADE",
        "DROP TABLE open_orders CASCADE",
        "DROP TABLE categories CASCADE"
    )

    for command in commands:
        cur.execute(command)

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()


delete_tables()