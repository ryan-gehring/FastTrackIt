import sqlite3
from sqlite3 import Error

database = r"data/pythonsqlite.db"

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
    
conn = create_connection(database)

clear_database(database,conn)