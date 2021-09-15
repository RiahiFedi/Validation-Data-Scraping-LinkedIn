# -*- coding: utf-8 -*-
"""
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


driver = webdriver.Chrome(parameters.webdriver_Chrome_path)
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)
sleep(random.randint(500,1000)/1000)
password = driver.find_element_by_id('session_password')
password.send_keys(parameters.linkedin_password)
sleep(random.randint(500,1000)/1000)
sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
sign_in_button.click()

url_fl = open(parameters.urls_file_name, "r")
urls = []
for line in url_fl:
  stripped_line = line.strip()
  urls.append(stripped_line)
url_fl.close()

'''urls = ['https://www.linkedin.com/posts/attijari-bank-tunisie_attijaribank-croireabrenabrvous-activity-6802540435110678528-aspH',\
        'https://www.linkedin.com/posts/stb-bank_cest-quoi-le-tmm-retrouvez-une-explication-activity-6741729911691706368-WYvB',
        'https://www.linkedin.com/posts/arabtunisianbank_atbabrmobile-activity-6759467489257697280-nqRB',
        'https://www.linkedin.com/posts/amen-bank_amen-first-bank-est-la-1%C3%A8re-banque-100-en-activity-6803375772187922432-CMx2',
        'https://www.linkedin.com/posts/zitouna-bank_vous-%C3%AAtes-un-professionnel-et-vous-cherchez-activity-6802516675674562560-i4by'
        ]'''
info = {'name' : [], 'linkedin_url' : [], 'reaction' : []}
for i in range(len(urls)):
    #driver.get('https://www.linkedin.com/posts/attijari-bank-tunisie_attijari-bank-espace-libre-service-bancaire-activity-6769179416443547648-N-K0/')
    #driver.get('https://www.linkedin.com/posts/zitouna-bank_banque-zitouna-continue-%C3%A0-d%C3%A9velopper-ses-activity-6793113131682955264-Kisi/')
    driver.get(urls[i])
    sleep(random.randint(500,1000)/1000)
    scroll_down()
    # locate the reactions pannel
    react_pannel = driver.find_element_by_class_name('social-details-social-counts')
    react_pannel = react_pannel.find_element(By.XPATH, '//li[1]/button')
    actions = ActionChains(driver)
    actions.move_to_element(react_pannel).perform()
    react_pannel.click()
    
    react_pannel = driver.find_element(By.XPATH, '//*[@class="artdeco-modal__content social-details-reactors-modal__content ember-view"]')
    allfoll=int(driver.find_element_by_xpath('//*[@class="ml0 p3 artdeco-tab active artdeco-tab--selected ember-view"]/div/span[2]').text)
    for i in range(int(allfoll//6)):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", react_pannel)
        sleep(random.randint(500,1000)/1000)
        
    sel = driver.page_source
    soup = BeautifulSoup(sel, 'lxml')
    place_holder = soup.find('div',{'class' : 'artdeco-modal__content social-details-reactors-modal__content ember-view'})
    profile_elements = place_holder.find_all('li',{'class' : 'artdeco-list__item'})
    
    
    
    
    
    for el in profile_elements:
        url = el.a['href']
        name = el.find('div',{'class' : 'artdeco-entity-lockup__title ember-view'}).span.text.strip()
        place_holder = el.find('div',{'class':'relative'})
        reaction  = place_holder.find_all('img')[-1]['alt']

        info['name'].append(name)
        info['linkedin_url'].append(url)
        info['reaction'].append(reaction)
        
    df = pd.DataFrame(data=info)
    #df.to_csv('reactions' + str(i) + '.csv')
df.to_csv('reactions.csv')
driver.quit()
