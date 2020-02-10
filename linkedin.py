import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import random
from lxml import html
from parsel import Selector

writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Company', 'Education', 'Location', 'URL'])


browser = webdriver.Chrome('chromedriver')
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
sleep(5)
username = browser.find_element_by_name("session_key")
username.send_keys('<username>')

password = browser.find_element_by_name('session_password')
password.send_keys('<password>')

sign_in_button = browser.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
sign_in_button.click()
sleep(2)

browser.get('https://www.linkedin.com/search/results/content/?keywords=oracle%20pl%20sql&origin=SWITCH_SEARCH_VERTICAL')
sleep(5)

total_height = browser.execute_script("return document.body.scrollHeight")
while True:    
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(random.uniform(2.5, 4.9))

    page = bs(browser.page_source, 'lxml')    
    content = page.find_all('li',{'class':'search-content__result search-entity ember-view'})
    for c in content:            
        try:
            print(c.find('a',{'class':'feed-shared-actor__container-link relative display-flex flex-grow-1 app-aware-link ember-view'}).get('href'))
        except:
            pass

        try:        
            print(c.find('div',{'class':'feed-shared-text__text-view feed-shared-text-view white-space-pre-wrap break-words ember-view'}).findNext('span').findNext('span',{'class':'ember-view'}).findNext('span').get_text())
        except:
            pass

        try:
            print(c.find('a',{'class':'feed-shared-article__meta flex-grow-1 full-width tap-target app-aware-link ember-view'}).get('href'))
        except:
            pass


browser.quit()     