#
# This will take the main page and open
# the links on it
#
# Goal is to use this in conjunction
# with the scraping tool to scrape all
# relevant auction pages
#

import requests
import datetime
import string

from scrape_sale import scrape_sale
from bs4 import BeautifulSoup

def crawl(locations):
    link='https://www.bidfta.com/bidderHome'
    page=requests.get(link)
    soup=BeautifulSoup(page.text, 'lxml')
    day=datetime.date.today().day

    auctions=soup.findAll('div', { 'class' : 'medium-4 columns auction' })
    for a in auctions:
        timeout=a.find('time').get('datetime')
        timeout=timeout[5:16]
        if int(timeout[3:5]) < day:
            continue

        location=a.find('p', class_="auctionLocation").find(text=True).lower()
        if not 'found' in ['found' if (loc in location) else None for loc in locations]:
            continue

        link=a.find('a').get('href')
        link=str.replace(link, "mndetails", "mnprint")
        print("{} | {} | {}".format(timeout, location, link))
        scrape_sale(link)
