import sqlite3
from sqlite3 import Error

def clear_database(db_file,conn):
    sql_clear_auctions = """
    DELETE FROM auctions
    """
    sql_clear_auction_items = """
    DELETE FROM auction_items
    """
    try:
        c = conn.cursor()
        c.execute(sql_clear_auctions)
        c.execute(sql_clear_auction_items)
    except Error as e:
        print(e)
    conn.commit()
    conn.close()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def setup_database(database_file):
     
    sql_create_auctions_table = """ 
    CREATE TABLE IF NOT EXISTS auctions (
    auction_id text PRIMARY KEY,
    auction_end text,
	auction_time_remaining text,
    auction_link text
    );"""
 
    sql_create_auction_items_table = """
    CREATE TABLE IF NOT EXISTS auction_items (
    item_lot_id text PRIMARY KEY,
    item_description text,
	item_status text,
	item_current_bid numeric,
	item_msrp numeric,
    item_link text,
	auction_id text,
    FOREIGN KEY (auction_id) REFERENCES auctions (auction_id)
    );"""
 
    # create a database connection
    conn = create_connection(database_file)
 
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_auctions_table)
 
        # create tasks table
        create_table(conn, sql_create_auction_items_table)
    else:
        print("Error! cannot create the database connection.")

    #cursor = conn.cursor()
    conn.commit()
    conn.close()

#### Add auction details from dict to database #####
def add_auction_details_to_database(all_auctions,cursor):
    for key,value in all_auctions.items():
        auction_id_value = key
        auction_end_value = value[0]
        auction_time_remaining_value = value[1]
        auction_link_value = value[2]
        in_statement = """
                    INSERT INTO auctions (auction_id, auction_end, auction_time_remaining, auction_link) 
                    VALUES (?,?,?,?);
                    """
        cursor.execute(in_statement, (auction_id_value,auction_end_value,auction_time_remaining_value,auction_link_value))

#### Add items from auction dict #####
def add_items_to_database(all_items_for_auction,auction_id,cursor):
    for key,value in all_items_for_auction.items():
        item_lot_id_value = key
        item_description_value = value[0]
        item_status_value = value[1]
        item_current_bid_value = value[2]
        item_msrp_value = value[3]
        item_link_value = value[4]
        auction_id_value = auction_id
        in_statement = """
                    INSERT INTO auction_items (item_lot_id, item_description, item_status, item_current_bid, item_msrp, item_link, auction_id) 
                    VALUES (?,?,?,?,?,?,?);
                    """
        cursor.execute(in_statement, (item_lot_id_value,item_description_value,item_status_value,item_current_bid_value,item_msrp_value,item_link_value,auction_id_value))