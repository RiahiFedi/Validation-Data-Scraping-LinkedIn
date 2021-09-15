# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:36:49 2021

@author: fedir
"""


from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import pandas as pd
from selenium.common.exceptions import WebDriverException


def scroll_down():
    SCROLL_PAUSE_TIME=4
    #height=driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight,left: 0,behavior: 'smooth'});")
    sleep(SCROLL_PAUSE_TIME)
    '''while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        max_height=driver.execute_script("return document.body.scrollHeight")
        if max_height == height:
            break
        height=max_height'''

driver = webdriver.Chrome('C:/Users/fedir/Data_Scraping_Linkedin/chromedriver')
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)
sleep(random.randint(500,1000)/1000)
password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(random.randint(500,1000)/1000)
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_button.click()




#url = 'https://www.linkedin.com/in/mathildesalles/'

#Getting reactions Linkedin urls
url_data = pd.read_csv('reactions.csv')
linkedin_urls = url_data['linkedin_url']
companies_info = pd.read_csv('companies_info.csv')

#url = linkedin_urls[51]
'''companies_info =pd.DataFrame(data= {
    'field':[],
    'comp_url':[]
    })'''
temp_l = list([''] * len(linkedin_urls))
url_data['interests'] = temp_l

for url in linkedin_urls:

    driver.get(url)
    sleep(random.randint(500,1000)/1000)
    for i in range(3) : 
        scroll_down()
    
    try:    
        link_to_interests_pannel = driver.find_element_by_xpath("//a[@data-control-name='view_interest_details']").get_attribute('href').strip()
        driver.get(link_to_interests_pannel + 'companies/')
        sleep(random.randint(500,1000)/1000)
        interests_pannel = driver.find_element_by_xpath("//div[@class='artdeco-modal__content ember-view']")
        for i in range(3):  
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", interests_pannel)
            sleep(random.randint(500,1000)/1000)    
    except WebDriverException:
        print('link does not exist')
        
    try: 
        sel = driver.page_source
        soup = BeautifulSoup(sel, 'lxml')
        place_holder = soup.find('div',{'class' : 'entity-list-wrapper ember-view'}).ul
        profile_elements = place_holder.find_all('li',{'class' : 'entity-list-item'})
    except AttributeError:
        print('getting list error')
    
    comp = profile_elements[2]
    str_interests = ''
    for comp in profile_elements:
        
        comp_url = comp.find('a',{'class':'pv-interest-entity-link ember-view'})['href']
        if not comp_url in list(companies_info['comp_url']):
            try:
                link = 'https://www.linkedin.com'  + comp_url
                driver.get(link)
                sleep(random.randint(500,1000)/1000)
                scroll_down()
                sel = driver.page_source
                soup = BeautifulSoup(sel, 'lxml')
                work_field = soup.find('div', {'class' : 'org-top-card-summary-info-list__info-item'}).text.strip()
            except AttributeError:
                print('getting fiel error')       
                work_field = ''
                
            companies_info =companies_info.append({'field' : work_field,'comp_url': comp_url},ignore_index=True)
        else:
            work_field = list(companies_info[companies_info['comp_url']==comp_url]['field'])[0]
        if not work_field in str_interests.split('-'):
            str_interests = str_interests+ work_field + '-'
            print(str_interests)
        print(str_interests)
    url_data['interests'][url_data['linkedin_url'] == url ] = str_interests

companies_info.to_csv('companies_info.csv')
url_data.to_csv('interests.csv')
driver.quit()
