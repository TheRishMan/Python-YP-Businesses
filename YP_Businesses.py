#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
start_time = time.time()

#Importing various libraries

con = sqlite3.connect(r"C:\Users\rishi\OneDrive\Documents\Programming\Python\Projects\YP_Business.db")
cur = con.cursor()
#Connecting to SQL Database

city_name = "Cleveland"
cur.execute("CREATE TABLE IF NOT EXISTS " + city_name + "(Name TEXT PRIMARY KEY, Category TEXT, Phone TEXT, Address TEXT)")
#Creating table
#Please change table name to proper city

res = requests.get("https://www.yellowpages.com/cleveland-tn")
src = res.content
soup = BeautifulSoup(src, 'lxml')
#Retrieving and parsing web content
#Please change url to correct city

section = soup.find('section' , {'class', 'popular-cats'})
for i in section.find_all('a'):
    res = requests.get("https://www.yellowpages.com" + i.get('href'))
    src = res.content
    soup = BeautifulSoup(src, 'lxml')
#Iterating through each link in the popular categories

    for i in soup.find_all('div', {'class', 'info'}):
        if ((i.h2.text)[0]).isdigit():
            name = i.h2.a.string
            try:
                cat = (i.find('div', {'class', 'categories'})).a.string
            except:
                cat = 'N/A'
            try:
                phone = (i.find('div', {'class', 'phones phone primary'})).string
            except:
                phone = 'N/A'
            try:
                addr = ''
                addr += (i.find('div', {'class', 'street-address'})).string
                addr += " "
                addr += (i.find('div', {'class', 'locality'})).string
            except:
                addr = city_name + " Area"
            cur.execute("INSERT OR IGNORE INTO " + city_name + " VALUES(?,?,?,?)", (name, cat, phone, addr))
#Retrieving data and inserting it into SQL Table

con.commit()
con.close()
#Saving changes and closing database

print(f"Run Time: {int(time.time() - start_time)} seconds")
