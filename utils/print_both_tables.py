import sqlite3
from sqlite3 import Error

database = r"../data/pythonsqlite.db"

def print_auctions_table(db_file,conn):
    sql_select_all_from_auctions = """
    SELECT * FROM auctions
    """

    try:
        c = conn.cursor()
        c.execute(sql_select_all_from_auctions)
        results = c.fetchall()
        print(results)
    except Error as e:
        print(e)
    conn.commit()

def print_auction_items_table(db_file,conn):
    sql_select_all_from_auctions = """
    SELECT * FROM auction_items
    """

    try:
        c = conn.cursor()
        c.execute(sql_select_all_from_auctions)
        results = c.fetchall()
        for each_item in results:
            print(each_item)
    except Error as e:
        print(e)
    conn.commit()
    
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

print_auctions_table(database,conn)
print_auction_items_table(database,conn)

conn.close()
