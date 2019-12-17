import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)




def setup_database():
    database = r"pythonsqlite.db"
 
 
    sql_create_auctions_table = """ CREATE TABLE IF NOT EXISTS auctions (
                                        auction_id text PRIMARY KEY,
                                        auction_end text,
									    auction_time_remaining text,
                                        auction_link text
                                    ); """
 
    sql_create_auction_items_table = """CREATE TABLE IF NOT EXISTS auction_items (
                                    item_lot_id text PRIMARY KEY,
                                    item_description text,
									item_status text,
									item_current_bid numeric,
									item_msrp numeric,
									auction_id text,
                                    FOREIGN KEY (auction_id) REFERENCES auctions (auction_id)
                                );"""
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_auctions_table)
 
        # create tasks table
        create_table(conn, sql_create_auction_items_table)
    else:
        print("Error! cannot create the database connection.")