# -*- coding: utf-8 -*-
"""
@author: fedir
"""

# imports
from selenium import webdriver
import csv
from time import sleep
import parameters 
from bs4 import BeautifulSoup
import pandas as pd
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os

# if field is present pass if field:pas if field is not present print text else:
def validate_field(field):
    if type(field) is not str:
       field = 'No results'
    return field


info = {'name' : [],
    'profile_title' : [], 
    'entreprise_name' : [],
    'duration' : [],
    'experience' : [],
    'location' : [],
    'education' : [],
    'nbr_employees' :[],
    'work_field' :[],
    'linkedin_url': []
    }
def get_driver():
    # specifies the path to the chromedriver.exe
    return webdriver.Chrome(parameters.webdriver_Chrome_path)

def login(initial_state = True):
    
    
    if not initial_state:
        print('lol')
    
        # specifies the path to the chromedriver.exe
        driver = get_driver()
         
        # driver.get method() will navigate to a page given by the URL address
        driver.get('https://www.linkedin.com')
        
        # locate email form by_class_name
        username = driver.find_element_by_id('session_key')
        
        # send_keys() to simulate key strokes
        username.send_keys(parameters.linkedin_username)
        
        # sleep for 0.5 seconds
        sleep(random.randint(500,1000)/1000)
        
        # locate password form by_class_name
        password = driver.find_element_by_id('session_password')
        
        # send_keys() to simulate key strokes
        password.send_keys(parameters.linkedin_password)
        sleep(random.randint(500,1000)/1000)
        
        # locate submit button by_xpath
        sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
        
        # .click() to mimic button click
        sign_in_button.click()
        
        return driver



def scroll_down(driver, initial_state = True):
    SCROLL_PAUSE_TIME = random.randint(500,1000)/1000
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
    if initial_state:
        driver.quit()



def scrap(driver,url_ = 'https://www.linkedin.com/in/fedi-riahi-46bb7b17a/',initial_state = True):
    
    if not initial_state:
        
        # specifies the path to the chromedriver.exe
        #driver = get_driver()
        #login(False)
        driver.get(url_)
        
        # add a 5 second pause loading each URL
        for i in range(3):
            sleep(random.randint(500,1000)/1000)
            scroll_down(driver,False)
        
        # assigning the source code for the webpage to variable sel
        sel = driver.page_source
        soup = BeautifulSoup(sel, 'lxml')
        
        
        try:
            exp_section=soup.find('section',{'id' : 'experience-section'})
            if len( exp_section.find_all('div',{'class' : 'pv-experience-section__see-more pv-profile-section__actions-inline ember-view'})) > 0:
                # locate the reactions pannel
                #more_pannel = driver.find_element_by_class_name('pv-experience-section__see-more pv-profile-section__actions-inline ember-view')
                more_pannel = driver.find_element(By.XPATH, '//*[@class="pv-experience-section__see-more pv-profile-section__actions-inline ember-view"]')
                actions = ActionChains(driver)
                actions.move_to_element(more_pannel).perform()
                more_pannel = more_pannel.find_elements(By.XPATH, '//*[@class="pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted"]')[-1]
                actions = ActionChains(driver)
                more_pannel.click()
            
            sel = driver.page_source
            soup = BeautifulSoup(sel, 'lxml')
        except AttributeError:
            print('no xp')
        #name_div=soup.find('div',{'class' : 'flex-1 mr5'})
        
            
        try:
            name_div=soup.find('div',{'class' : 'pv-text-details__left-panel mr5'})
            name_loc=name_div.find_all('div')
            
            name=name_loc[0].h1.text.strip()
            profile_title=name_loc[1].text.strip()
            location=name_loc[2].span.text.strip()
            
            big_div = soup.find('ul',{'class' : 'pv-text-details__right-panel'})
            place_holder = big_div.find_all('li')
            #place_holder = work_div[1].find_all('a', {'class' : 'pv-top-card--experience-list-item'})
            
            if len(place_holder)>1:
                entreprise_name = place_holder[0].a.h2.div.text.strip()
                education = place_holder[1].a.h2.div.text.strip()
            elif len(place_holder) == 1 :
                test = place_holder[0].a.h2.div['aria-label']
                if test == 'Current company':
                    entreprise_name = place_holder[0].a.h2.div.text.strip()
                    education = ''
                elif test == 'Education':
                    education = place_holder[0].a.h2.div.text.strip()
                    entreprise_name = 'Currently Unemployed'
            else: 
                education = ''
                entreprise_name = 'Currently Unemployed'
        except AttributeError:
            print('name') 
            
        try:
            exp_section=soup.find('section',{'id' : 'experience-section'}).ul.li
            if not exp_section.find_all('ul'):
            #place_holder = exp_section.find_all('div',{'class' : 'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})
                place_holder = exp_section.find('h4')
                place_holder = place_holder.find_all('span')
                Duration = place_holder[1].text.strip()
            else:
                place_holder = exp_section.find_all('ul')[0].find_all('li')
                
                if len(place_holder[0].find_all('div',{'class' : 'display-flex'})) > 1 :
                    last_ = place_holder[0].find_all('div',{'class' : 'display-flex'})[1].h4.find_all('span')[1].text.strip()
                    first_ = place_holder[-1].find_all('div',{'class' : 'display-flex'})[1].h4.find_all('span')[1].text.strip()
                    
                else:
                    last_ = place_holder[0].find('div',{'class' : 'display-flex'}).h4.find_all('span')[1].text.strip()
                    first_ = place_holder[-1].find('div',{'class' : 'display-flex'}).h4.find_all('span')[1].text.strip()
                
                dates = first_.split('–') + last_.split('–')
                Duration = dates[0] + '–' + dates[-1]
                
        except AttributeError:
            print('duration')
            Duration=''
            #job_title=''
            #job_duration=''
     
        '''try:
            place_holder =soup.find('section', {'class' : 'pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view'}).ul
            elements = place_holder.find_all('li', {'class' : 'pv-interest-entity pv-profile-section__card-item ember-view'})
                
        except AttributeError:
            interests = '''
            
        try :
            exp_section=soup.find('section',{'id' : 'experience-section'}).ul
            job_list = exp_section.find_all('li',{'class':'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})
            if not job_list[-1].find_all('ul'):
                place_holder = job_list[-1].find('h4')
                place_holder = place_holder.find_all('span')
                first_job = place_holder[1].text.strip()
                dates = first_job.split('–') + Duration.split('–')
                total_exp = dates[0] + '–' + dates[-1]
            else:
                place_holder = job_list[-1].find_all('ul')[0].find_all('li')
                if len(place_holder[0].find_all('div',{'class' : 'display-flex'})) > 1 :
                    first_job = place_holder[-1].find_all('div',{'class' : 'display-flex'})[1].h4.find_all('span')[1].text.strip()
                    
                else:
                    first_job = place_holder[-1].find('div',{'class' : 'display-flex'}).h4.find_all('span')[1].text.strip()
                
        except AttributeError: 
            total_exp = ''       
    
    
            
           
            
        try :
            exp_section = soup.find('section',{'id' : 'experience-section'})
            if exp_section.find_all('a',{'class' : 'full-width ember-view'}):
                link = exp_section.find_all('a',{'class' : 'full-width ember-view'})[0]['href']
            else : raise AttributeError
            if link[0:8] != '/company' :
                print('no')
                work_field = ''
                nbr_employees = ''
            else: 
                link = 'https://www.linkedin.com'  + link
                driver.get(link)
                sleep(random.randint(500,1000)/1000)
                scroll_down(driver,False)
                sel = driver.page_source
                soup = BeautifulSoup(sel, 'lxml')
                work_field = soup.find('div', {'class' : 'org-top-card-summary-info-list__info-item'}).text.strip()
                place_holder = soup.find('div', {'class': 'mt1'}).div
                nbr_employees = place_holder.find_all('a', {'class' : 'ember-view'})[-1].span.text.strip()
                l_temp = re.findall(r'\b\d+\b', nbr_employees)
                if len(l_temp)>1:
                    nbr_employees = int(l_temp[0])*1000+ int(l_temp[1])
                else:
                    nbr_employees = int(l_temp[0])
                #nbr_employees = [int(s) for s in nbr_employees.split() if s.isdigit()][0]
        except AttributeError:
            work_field = ''
            nbr_employees = ''
        driver.quit()
            
        return {
        'name' : name,
        'profile_title' : profile_title,
        'entreprise_name':entreprise_name,
        'duration':Duration,
        'experience':total_exp,
        'location':location,
        'education':education,
        'linkedin_url':url_,
        'work_field':work_field,
        'nbr_employees':nbr_employees}
        driver.quit()
    # terminates the application


#Saves the data as a csv file
def save_res():
    
    df = pd.DataFrame(data=info)
    df.to_csv('results_file.csv', encoding = 'utf-8-sig')


