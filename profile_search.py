# -*- coding: utf-8 -*-
"""
@author: fedir
"""
# imports
from selenium import webdriver
import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
import parameters 

def scroll_down():
    SCROLL_PAUSE_TIME=2
    height=driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight,left: 0,behavior: 'smooth'});")
    sleep(SCROLL_PAUSE_TIME)

linkedin_urls = []

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(parameters.webdriver_Chrome_path)

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com/intl/en/')
sleep(0.5)

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys(parameters.search_query)
sleep(0.5)

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)
sleep(0.5)

for i in range(32):
    
    scroll_down()

    
    # locate URL by_class_name
    raw_linkedin_urls = driver.find_elements_by_class_name('yuRUbf')
    
    # variable linkedin_url is equal to the list comprehension 
    for url in raw_linkedin_urls:
        linkedin_urls.append(url.find_element_by_css_selector('a').get_attribute('href'))
    
    #Going to the next results page
    try:
        next_page_url = driver.find_element_by_id('pnnext').get_attribute('href')
        driver.get(next_page_url)
    except NoSuchElementException:
        break
    sleep(0.5)
    

driver.quit()



# Saving the collecte urls into a text file
urls_fl = open(parameters.random_urls_file_name, 'w')
linkedin_urls=map(lambda x:x+'\n', linkedin_urls)
urls_fl.writelines(linkedin_urls)
urls_fl.close()
