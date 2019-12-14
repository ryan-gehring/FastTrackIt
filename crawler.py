from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import urllib.request
import time
import pandas as pd

#Define
bid_fta_homepage = 'https://www.bidfta.com/'
bid_fta_all_auctions = 'https://www.bidfta.com/home'
zip_code = 45236
city = 'Cincinnati'

#Driver Options
browser = "FIREFOX" #FIREFOX or CHROME
headless = False #Open the browser in headless mode = True
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

def setup_driver (headless,browser,implicitly_wait):
	if headless:
		driver_options = Options()
		driver_options.headless = True
		driver = webdriver.Firefox(options=driver_options)
	else:
		driver = webdriver.Firefox()
	
	driver.implicitly_wait(15)
	return driver

def filter_auctions_by_zip(driver,bid_fta_homepage,zip_code):
	#Wait action Timeout explicit when needed
	wait = WebDriverWait(driver, 10)

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

	#Print all auction results on page
	results = driver.find_elements_by_xpath("//*[@class='col-xs-12 col-sm-6 col-md-4 col-lg-3 product-list padd-0 slick-slide slick-active']")
	print("==========================================================================")
	for eachAuction in results:
		print(eachAuction.text)

def get_all_auctions_filtered_locations(driver,bid_fta_all_auctions,city):

	#From dropdown select anything with cincinnati
	driver.get(bid_fta_all_auctions)
	warehouse_dropdown = driver.find_element_by_xpath("//*[@class='multiselect-container dropdown-menu']")
	warehouses = warehouse_dropdown.find_elements_by_tag_name("li")
	print("==========================================================================")
	for warehouse in warehouses:
		warehouse_location = warehouse.find_element_by_class_name("checkbox")
		print(warehouse_location.get_attribute("title"))

def clean_up ():
	driver.quit()

#Run it
driver = setup_driver (headless,browser,implicitly_wait)
get_all_auctions_filtered_locations(driver,bid_fta_all_auctions,city)
#filter_auctions_by_zip(driver,bid_fta_homepage)
#clean_up()