from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import time
import pandas as pd
import database

#Define
bid_fta_homepage = 'https://www.bidfta.com/'
bid_fta_all_auctions = 'https://www.bidfta.com/home'

def change_page (driver,wait,page_num):
	page_input = driver.find_element_by_id("pageInput")
	page_input.send_keys(page_num)
	
	#Click Go button
	go_button = driver.find_element_by_id("pagebtn")
	go_button.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)

def clean_up (driver):
	driver.quit()

def filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city):
	#Open the Webpage
	driver.get(bid_fta_all_auctions)

	#Expand the warehouse location dropdown
	clickable_warehouse_dropdown = driver.find_element_by_xpath("//*[@class='multiselect dropdown-toggle btn btn-default']")
	clickable_warehouse_dropdown.click()

	#Find all the dropdown options
	warehouse_dropdown = driver.find_element_by_xpath("//*[@class='multiselect-container dropdown-menu']")
	warehouses = warehouse_dropdown.find_elements_by_tag_name("li")

	#Loop through the warehouse locations for any containing the city of interest and select them
	for warehouse in warehouses:
		warehouse_location = warehouse.find_element_by_class_name("checkbox")
		warehouse_location_name = warehouse_location.get_attribute("title")
		if city in warehouse_location_name:
			#Checks that the warehouse location isnt already selected since we dont want it to de-select it
			warehouse_location_classes = warehouse.get_attribute("class")
			if "active" not in warehouse_location_classes:
				warehouse.click()
	
	#Click the filter button
	filter_button = driver.find_element_by_xpath("//*[@class='btn btn-lg btn-style filter-btn']")
	filter_button.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)

def get_all_auctions_on_page (driver,wait):
	#Print all auction results on page bidfta.com/home
	auction_dictionary = {}
	auction_details = []
	all_auctions = driver.find_elements_by_xpath("//div[starts-with(@id,'auctionContainer')]")

	#Record details for each auction
	for each_auction in all_auctions:
		auction_id = each_auction.find_element_by_xpath(".//p[starts-with(text(),'Auction:')]").text.split(': ')[1]
		auction_end = each_auction.find_element_by_xpath(".//div[contains(@class,'endTime')]").text
		auction_time_remaining = each_auction.find_element_by_xpath(".//span[starts-with(@id,'time')]").text
		auction_link = each_auction.find_element_by_xpath(".//a[starts-with(@href,'/auctionDetails')]").get_attribute("href")
		auction_details = [auction_end,auction_time_remaining,auction_link]
		auction_dictionary[auction_id] = auction_details

	return auction_dictionary
	
def get_total_pages (driver):
	total_pages = driver.find_element_by_xpath("//span[@class='total total_page']")
	#print(total_pages.text)

	return int(total_pages.text)

def navigate_to_auction_items_by_auction_id(driver,auction_id,auction_dictionary):
	#Get auction dictionary items
	auction_details = auction_dictionary.get(auction_id)
	auction_link = auction_details[2]
	auction_link_num = auction_link[-5:]
	auction_items_link = "https://www.bidfta.com/auctionItems?listView=true&idauctions=" + auction_link_num + "&pageId=1"
	driver.get(auction_items_link)

def get_all_items_on_page(driver):
	item_dictionary = {}
	item_details = []
	all_items_on_page = driver.find_elements_by_xpath("//div[starts-with(@id,'itemContainer')]")

	#Record details for each auction
	for each_item in all_items_on_page:
		#Find the item details we are interested in
		item_lot_id = each_item.find_element_by_xpath(".//span[starts-with(@id,'lotcode')]").text
		item_description = each_item.find_element_by_xpath(".//p[contains(@class,'title')]").text
		item_status = each_item.find_element_by_xpath(".//p[contains(@class,'itemStatus')]").text
		item_current_bid = each_item.find_element_by_xpath(".//span[starts-with(@id,'currentBid')]").text.split('$')[1]
		item_msrp_raw = each_item.find_element_by_xpath(".//div[contains(@class,'text-right')]").text
		if item_msrp_raw:
			item_msrp = item_msrp_raw.split('$ ')[1]
		else:
			item_msrp = None

		#Use the lot_id as a key and the rest of the details as values
		item_details = [item_description,item_status,item_current_bid,item_msrp]
		item_dictionary[item_lot_id] = item_details

	return item_dictionary

def get_all_items_by_auction_id(driver,wait,auction_id,auction_dictionary):
	#Navigate to item page for a specific auction
	navigate_to_auction_items_by_auction_id(driver,auction_id,auction_dictionary)

	#Get the number of result pages
	total_result_pages = get_total_pages (driver)

	#Scan all pages and pull auction info into new dictionary
	all_items_dict = {}
	for i in range(2, total_result_pages+1):
		all_items_dict.update(get_all_items_on_page(driver))
		change_page(driver,wait,i)

	#Get final page
	all_items_dict.update(get_all_items_on_page(driver))

	return all_items_dict

#Finish building this function to loop through all auctions and get items.
def add_items_to_all_auctions(driver,wait,auction_dictionary):

	database.setup_database()
	conn = database.create_connection('data/pythonsqlite.db')
	cursor = conn.cursor()

	#Add auction details to database
	database.add_auction_details_to_database(auction_dictionary,cursor)

	for key,value in auction_dictionary.items():
		auction_id_value = key
        #auction_end_value = value[0]
        #auction_time_remaining_value = value[1]
        #auction_link_value = value[2]
		all_items_for_auction = get_all_items_by_auction_id(driver,wait,auction_id_value,auction_dictionary)
		
		#Add auction items to database
		database.add_items_to_database(all_items_for_auction,auction_id_value,cursor)


	#Add items to auction_dictionary
	#auction_details.extend(item_details)
	#auction_dictionary_with_items[auction_id] = auction_details

	conn.commit()
	cursor.close()
	conn.close()

	return None #auction_dictionary_with_items


def find_all_auctions_by_city(driver,wait,city):
	auction_dictionary = {}
	filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city)
	#Get the number of result pages
	total_result_pages = get_total_pages (driver)
	#Scan all pages and pull auction info
	for i in range(2, total_result_pages+1):
		auction_dictionary.update(get_all_auctions_on_page(driver,wait))
		change_page(driver,wait,i)
	#Get final page
	auction_dictionary.update(get_all_auctions_on_page(driver,wait))

	return auction_dictionary

def setup_driver (headless,browser,implicitly_wait):
	if headless:
		driver_options = Options()
		driver_options.headless = True
		driver = webdriver.Firefox(options=driver_options)
	else:
		driver = webdriver.Firefox()
	
	actions = ActionChains(driver)
	#Wait time when using explicit wait
	wait = WebDriverWait(driver, 10)
	driver.implicitly_wait(10)
	return driver,actions,wait




#Planning to delete, but saving for short term reference
''' Probably should delete this, was my first attempt at scraping a page and we dont really need this page
def filter_auctions_by_zip(driver,wait,bid_fta_homepage,zip_code):
	#Probably wont use this function. Will use the all auctions page instead
	driver.get(bid_fta_homepage)

	#Fill out zipcode and search radius(miles)
	zip_code_field = driver.find_element_by_id("zip")
	zip_code_field.send_keys(zip_code)
	milesRadius = Select(driver.find_element_by_id("miles"))
	milesRadius.select_by_value('50')
	#Click button to apply filter
	filterButton = driver.find_element_by_class_name("filterAuction")
	filterButton.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)
'''

''' Dont think I'll use this either, it was a way to store things in a dictionary vs a database. Database seems like a better option.
def add_all_items_to_auction(driver,wait,auction_id,auction_dictionary):
	#Navigate to item page for a specific auction
	navigate_to_auction_items_by_auction_id(driver,auction_id,auction_dictionary)

	#Get the number of result pages
	total_result_pages = get_total_pages (driver)

	#Scan all pages and pull auction info into new dictionary
	all_items_dict = {}
	for i in range(2, total_result_pages+1):
		all_items_dict.update(get_all_items_on_page(driver))
		change_page(driver,wait,i)

	#Get final page
	all_items_dict.update(get_all_items_on_page(driver))
	
	#Get auction dictionary items
	auction_details = auction_dictionary.get(auction_id)
	
	#Add the items to the values for that auction_id
	auction_details.extend(all_items_dict)

	#Add that item-dictionary to the auction-dictionary
	auction_dictionary[auction_id] = auction_details

	return auction_dictionary
'''