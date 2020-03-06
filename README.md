# Scrape Linkedin content for job

Linkedin is for professional networking. it is also used by employers for posting jobs. There are cases where recruiters post job on there page which can be searched as content. When i was searching job, i found many jobs were posted by recruiter as post. To search such job, one has to search content. I tried to automate the same by scraping the content using python, selenium and beautifulsoup.  

## Requirement
1. [Python 3.x](https://www.python.org/)
2. [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
3. [Selenium](https://www.selenium.dev/)

All the dependencies can be installed using requirement file
```python
pip install -r requirements.txt
```

Let us go through the code.  

For scraping linkedin content, i have used selenium to browse the page. Selenium uses web driver, i have chosen chrome web driver for this, which can be downloaded from [chrome web driver](https://chromedriver.chromium.org/downloads). But since i am trying to automate the whole stuff, i have added a piece code which will check for chrome webdriver first and if it is not present then it will download latest one, unzip it and place it in current working directory. It is always better to use latest chrome web driver with latest chrome browser. For this, this script will check if chrome web driver used is more than 7 day old, then it will download latest one and replace the old one.

Module driver has a python file chromedriver.py, it has two function, get_chrome_driver_release for getting the latest chrome driver release version
```python
def get_chrome_driver_release():
    result = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
    return result.text
```
and download_driver for downloading the chrome driver.
```python
def download_driver(version):
    driver_download_url= 'https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip'.format(version)
    chrome_req = requests.get(driver_download_url)
    driver_zipfile = zipfile.ZipFile(io.BytesIO(chrome_req.content))
    driver_zipfile.extractall()
```
In case one wish to download driver manually, above code piece can be ignored.  

Let us start with main file ScrapeLinkedin.py code. On top all needed import statements are included.
```python
import time
import datetime
import csv
import os
import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from driver import chromedriver
```
Get current working directory path to locate chrome web driver.
```python
cur_dir_path=os.getcwd()
path_to_driver=os.path.join(cur_dir_path,'chromedriver')
```
Check if chrome web driver is present, if not then download latest one. In case driver is older than 7 days then also download latest one. In case of any error, re-raise the execption to stop the program.  
```python
try:
    if os.path.isfile(path_to_driver):            
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
```
Define max time for scrolling linkedin content page based on your need. It is good idea to set as linkedin content pages will have lot of contents.  
```python
endTime = time.time() + 60*5 # 5 min
```
Using csv writer, create output.csv file with header for writing scrapped content.
```python
writer = csv.writer(open('output\output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Profile', 'Description', 'Job URL'])
```
Open linkedin login page using chrome web driver. Since page loading takes sometime, i have used 5 sec sleep option.
```python
browser = webdriver.Chrome('chromedriver')
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
sleep(5)
```
Enter username, password and login.
```python
username = browser.find_element_by_name("session_key")
username.send_keys('<username>')

# pass password
password = browser.find_element_by_name('session_password')
password.send_keys('<password>')

# click on login button
sign_in_button = browser.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
sign_in_button.click()
sleep(2)
```
Open job search url. You can also prepare your own url, by logging into linkedin and searching content for specific keyword.
```python
browser.get('https://www.linkedin.com/search/results/content/?keywords=oracle%20pl%20sql&origin=SWITCH_SEARCH_VERTICAL')
```
Get page height for scrolling the page.
```python
total_height = browser.execute_script("return document.body.scrollHeight")
```
Start loop till the above defined max time.
```python
while time.time() < endTime:    
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    # set random sleep to avoid bot detection and blocking by linkedin
    sleep(random.uniform(2.5, 4.9))
    
    # get the page source using beautifulsoup
    page = bs(browser.page_source, 'lxml')    
    content = page.find_all('li',{'class':'search-content__result search-entity ember-view'})
    
    # loop through all content block and extract data, findNext for searching nested html elements contents beautifulsoup
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
```

Feel free to download the source code and try scraping linkedin content for jobs. Let me know in case you have any suggestion or feedback to improve the code. In next version, i will try to add job filter to store only those job content which are matching with individual profile.

Happy job hunting!
