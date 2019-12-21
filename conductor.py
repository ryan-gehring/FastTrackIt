import crawler
import database

#############################
#####   Define options  #####
#############################

#zip_code = 45236 Should delete this long term, not planning to use zip code page
city = 'Cincinnati'
browser = "FIREFOX" #FIREFOX or CHROME. Havent tested with Chrome yet
headless = False #Open the browser in headless mode = True/False
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

#############################
######   Web Scraping  ######
#############################
#Driver setup
driver,actions,wait = crawler.setup_driver(headless,browser,implicitly_wait)
#Get all auctions
all_auctions = crawler.find_all_auctions_by_city(driver,wait,city)

#Statically set auction_id for this test
auction_id = list(all_auctions.keys())[0]

#Pull items for one auction - This just gets one auctions items
#Using this while testing so it doesnt recursively grab all auctions items. Need to build function to do that for production
all_items_for_auction = crawler.get_all_items_by_auction_id(driver,wait,auction_id,all_auctions)

#############################
##### Database Fuctions #####
#############################
#Create empty database with auction and auction_items table
database.setup_database()
conn = database.create_connection('data/pythonsqlite.db')
cursor = conn.cursor()

#Add auction details to database
database.add_auction_details_to_database(all_auctions,cursor)

#Add auction items to database
database.add_items_to_database(all_items_for_auction,auction_id,cursor)

#############################
#####      Cleanup      #####
#############################
conn.commit()
cursor.close()
conn.close()
crawler.clean_up(driver)

'''
#Get one page of auctions for cincinnati
#filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city)
#one_page_of_auctions = get_all_auctions_on_page (driver,wait)
#print(one_page_of_auctions)

#Get all pages of auctions for cincinnati
#all_auctions = find_all_auctions_by_city(driver)
#print(all_auctions.keys())

#Get one page of items from auction
#page_of_items = get_all_items_on_page_by_auction_id(driver,list(all_auctions.keys())[0],all_auctions)
#print(len(page_of_items))

#clean_up()
'''