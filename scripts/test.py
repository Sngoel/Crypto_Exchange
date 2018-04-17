def test():
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

    cur.execute("INSERT INTO open_orders (user_id, coin_id, order_type ,amount, order_time) VALUES( %s, %s,%s, %s, %s);", (user_id, coin_id, order_type ,amount, order_time))

    #Destroy connection
    cur.close()
    conn.commit()
    conn.close()
