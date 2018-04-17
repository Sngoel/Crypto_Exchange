import psycopg2
import sys

def main():

    #Define our connection parameters
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"

    #Connect to database
    conn = psycopg2.connect(conn_string)

    #Initialize cursor
    cur = conn.cursor()

    tableshows = """SELECT coin_id FROM coins"""

    for tableshow in tableshows:
          cur.execute(tableshow)
          print(tableshow)

      #Destroy connection
    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
