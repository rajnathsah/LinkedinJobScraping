import time
import datetime
import csv
import os
import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from driver import chromedriver

# check if chromedriver exist else download latest version
cur_dir_path=os.getcwd()
path_to_driver=os.path.join(cur_dir_path,'chromedriver')

try:
    if os.path.isfile(path_to_driver):
        '''Check chromedriver last modified date and if older than 7 days then download 
        latest driver and place it in current working directory            
        '''            
        chrome_driver_last_mod = datetime.datetime.today() - datetime.datetime.utcfromtimestamp(os.path.getctime('chromedriver.exe'))
        if chrome_driver_last_mod > datetime.timedelta(days = 7):                
            chrome_release = chromedriver.get_chrome_driver_release()
            chromedriver.download_driver(chrome_release)
    else:
        chrome_release = chromedriver.get_chrome_driver_release()
        chromedriver.download_driver(chrome_release)
except Exception as ex:
    print('Error in finding/downloading chromedriver : {}-{}'.format(path_to_driver,ex))
    raise

# set max time for scrolling
endTime = time.time() + 60*5 # 5 min

# create output.csv file with heading
writer = csv.writer(open('output\output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Profile', 'Description', 'Job URL'])

# using chrome webdriver open browser and open linkedin login page
browser = webdriver.Chrome('chromedriver')
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
sleep(5)

# pass username
username = browser.find_element_by_name("session_key")
username.send_keys('<username>')

# pass password
password = browser.find_element_by_name('session_password')
password.send_keys('<password>')

# click on login button
sign_in_button = browser.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
sign_in_button.click()
sleep(2)

# open linkdin content search url
browser.get('https://www.linkedin.com/search/results/content/?keywords=oracle%20pl%20sql&origin=SWITCH_SEARCH_VERTICAL')
sleep(5)

# get the scroll height
total_height = browser.execute_script("return document.body.scrollHeight")

# run loop until time or change condition to True to scroll till end of content
#while True:
while time.time() < endTime:    
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    # set random sleep to avoid bot detection and blocking by linkedin
    sleep(random.uniform(2.5, 4.9))
    
    # get the page source using beautifulsoup
    page = bs(browser.page_source, 'lxml')    
    content = page.find_all('li',{'class':'search-content__result search-entity ember-view'})
    
    # loop through all content block and extract data
    for c in content:            
        try:
            profile_url = c.find('a',{'class':'feed-shared-actor__container-link relative display-flex flex-grow-1 app-aware-link ember-view'}).get('href')
        except:
            profile_url = ''        
        
        try:        
            description = c.find('div',{'class':'feed-shared-text__text-view feed-shared-text-view white-space-pre-wrap break-words ember-view'}).findNext('span').findNext('span',{'class':'ember-view'}).findNext('span').get_text()
        except:
            description = ''
                
        try:
            job_url = c.find('a',{'class':'feed-shared-article__meta flex-grow-1 full-width tap-target app-aware-link ember-view'}).get('href')
        except:
            job_url = ''
        
        # write data in csv file
        writer.writerow([profile_url, description, job_url])        
        
browser.quit()