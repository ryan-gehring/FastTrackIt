import crawler
import database

database.setup_database()
conn = database.create_connection('pythonsqlite.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
result = cur.fetchall()
print(result)





'''
#Run it
driver,actions,wait = setup_driver (headless,browser,implicitly_wait)

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


#Testing
#Get all auctions
all_auctions = find_all_auctions_by_city(driver)

#Statically set auction_id for this test
auction_id = list(all_auctions.keys())[0]

#Pull items for one auction
auction_dictionary_with_items = add_all_items_to_auction(driver,auction_id,all_auctions)
print(auction_dictionary_with_items[auction_id])
try:
	print(type(auction_dictionary_with_items[auction_id][3]))
except:
	print()
try:
	print(auction_dictionary_with_items[auction_id][3]['RED0173404'])
except:
	print()
'''