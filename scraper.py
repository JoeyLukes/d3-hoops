# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

s = Service("C:\Program Files (x86)\chromedriver.exe") ## get webdriver from localfiles
driver = webdriver.Chrome(service=s) ## instantiate driver

driver.get("https://libertyleagueathletics.com/calendar.aspx?path=mbball") ## get site link for composite schedule
#print(driver.title)
time.sleep(5)

n = 1
box_score_links = []
conf_games = driver.find_elements(by=By.CLASS_NAME, value="sidearm-calendar-conf-logo") ## retrieve all rows in composite schedule where the location field is denoted with '(Conf.)'
for game in conf_games:
    location_box = game.find_element(by=By.XPATH, value='..')
    links_box = location_box.find_element(by=By.XPATH, value='./following-sibling::td')
    try:
        link_text = links_box.find_element(by=By.TAG_NAME, value = 'span')
        link = link_text.find_element(by=By.LINK_TEXT, value='Box Score').get_attribute('href')
    except:
        print('game', n, 'has no link')
        pass
    print(n, link)
    #print(link_text.get_attribute('outerHTML'))
    box_score_links.append(link)

    n += 1
    # if n >= 2:
    #     break
print(box_score_links)