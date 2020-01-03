import crawler
import database

#############################
#####   Define options  #####
#############################
city = 'Cincinnati'
browser = "FIREFOX" #FIREFOX or CHROME. Havent tested with Chrome yet
headless = False #Open the browser in headless mode = True/False
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

#############################
##### Database Fuctions #####
#############################
#Create empty database with auction and auction_items table
database.setup_database()
connection = database.create_connection('data/pythonsqlite.db')

#############################
######   Web Scraping  ######
#############################
#Driver setup
driver,actions,wait = crawler.setup_driver(headless,browser,implicitly_wait)

#Get all auctions
all_auctions = crawler.find_all_auctions_by_city(driver,wait,city)

#Add items to all auctions
crawler.add_items_to_all_auctions(driver,wait,all_auctions,connection)

#############################
#####      Cleanup      #####
#############################
connection.close()
crawler.clean_up(driver)