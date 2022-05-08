## Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

## Beautiful Soup Imports
import requests
from bs4 import BeautifulSoup

## Pandas Imports
import pandas as pd

s = Service("C:\Program Files (x86)\chromedriver.exe") ## get webdriver from localfiles
driver = webdriver.Chrome(service=s) ## instantiate driver

driver.get("https://libertyleagueathletics.com/calendar.aspx?path=mbball") ## get site link for composite schedule
#print(driver.title)
time.sleep(5)

n = 1
box_score_links = [] ## empty list that will hold all of the links of valid box scores
conf_games = driver.find_elements(by=By.CLASS_NAME, value="sidearm-calendar-conf-logo") ## retrieve all rows in composite schedule where the location field is denoted with '(Conf.)'
for game in conf_games:
    location_box = game.find_element(by=By.XPATH, value='..') ## get the parent element of the conf_games variable (the row/game that conference game is apart of in the table)
    links_box = location_box.find_element(by=By.XPATH, value='./following-sibling::td') ## get the td element that is next to the location box, this is always where the box score link is
    try: 
        link_text = links_box.find_element(by=By.TAG_NAME, value = 'span') ## Sometimes there is no box score link (if the game is cancelled), so you need to try this first
        link = link_text.find_element(by=By.LINK_TEXT, value='Box Score').get_attribute('href') ## get the actual html link
    except:
        #print('game', n, 'has no link')
        pass ## if there is no link, pass
    box_score_links.append(link) ## append the link to the empty list


df_list = [] ## list that the df will be derived from. Will be a list of dictionaries where every row is a dictionary in the box score

n = 0 ## initiate counter for game id
for game in box_score_links: ## for each box score link 
    driver.get(game) ## get the webpage that the box score is on
    box_score = driver.find_element(by=By.ID, value='box-score') ## get the element that contains all of the box score information
    #print(box_score.get_attribute('outerHTML'))
    date = box_score.find_element(by=By.XPATH, value='//*[@id="box-score"]/header/div/div[2]/aside/dl/dd[1]').text ## save the date for this game as a variable
    away_team = box_score.find_element(by=By.XPATH, value='//*[@id="box-score"]/header/div/div[1]/table/tbody/tr[1]/th').text ## save the away team for this game as a variable
    away_score = box_score.find_element(by=By.XPATH, value='//*[@id="box-score"]/header/div/div[1]/table/tbody/tr[1]/td[3]').text ## save the away score for this game as a variable
    home_team = box_score.find_element(by=By.XPATH, value='//*[@id="box-score"]/header/div/div[1]/table/tbody/tr[2]/th').text ## save the home team for this game as a variable
    home_score = box_score.find_element(by=By.XPATH, value='//*[@id="box-score"]/header/div/div[1]/table/tbody/tr[2]/td[3]').text ## save the home score for this game as a variable

    for away_player in box_score.find_element(by=By.XPATH, value='//*[@id="DataTables_Table_0"]/tbody').find_elements(by=By.TAG_NAME, value='tr'): ## for each player on the away team
        df_row = {} ## create empty dictionary, get table information for each player on the away team in the box score, and add it as a key value pair in the dictionary
        df_row['GAME_ID'] = n
        df_row['DATE'] = date
        df_row['AWAY_TEAM'] = away_team
        df_row['AWAY_SCORE'] = away_score
        df_row['HOME_TEAM'] = home_team
        df_row['HOME_SCORE'] = home_score
        df_row['TEAM'] = away_team
        df_row['NUM'] = away_player.find_element(by=By.XPATH, value='./td[1]').text
        df_row['NAME'] = away_player.find_element(by=By.XPATH, value='./th').text
        df_row['GS'] = away_player.find_element(by=By.XPATH, value='./td[2]').text
        df_row['MIN'] = away_player.find_element(by=By.XPATH, value='./td[3]').text
        df_row['FGM'] = away_player.find_element(by=By.XPATH, value='./td[4]').text.split('-')[0]
        df_row['FGA'] = away_player.find_element(by=By.XPATH, value='./td[4]').text.split('-')[1]
        df_row['3PTM'] = away_player.find_element(by=By.XPATH, value='./td[5]').text.split('-')[0]
        df_row['3PTA'] = away_player.find_element(by=By.XPATH, value='./td[5]').text.split('-')[1]
        df_row['FTM'] = away_player.find_element(by=By.XPATH, value='./td[6]').text.split('-')[0]
        df_row['FTA'] = away_player.find_element(by=By.XPATH, value='./td[6]').text.split('-')[1]
        df_row['ORB'] = away_player.find_element(by=By.XPATH, value='./td[7]').text.split('-')[0]
        df_row['DRB'] = away_player.find_element(by=By.XPATH, value='./td[7]').text.split('-')[1]
        df_row['TREB'] = away_player.find_element(by=By.XPATH, value='./td[8]').text
        df_row['PF'] = away_player.find_element(by=By.XPATH, value='./td[9]').text
        df_row['A'] = away_player.find_element(by=By.XPATH, value='./td[10]').text
        df_row['TO'] = away_player.find_element(by=By.XPATH, value='./td[11]').text
        df_row['BLK'] = away_player.find_element(by=By.XPATH, value='./td[12]').text
        df_row['STL'] = away_player.find_element(by=By.XPATH, value='./td[13]').text
        df_row['PTS'] = away_player.find_element(by=By.XPATH, value='./td[14]').text

        df_list.append(df_row) ## append the player row to df_list

    for home_player in box_score.find_element(by=By.XPATH, value='//*[@id="DataTables_Table_1"]/tbody').find_elements(by=By.TAG_NAME, value='tr'): ## for each player on the home team
        df_row = {} ## create empty dictionary, get table information for each player on the home team in the box score, and add it as a key value pair in the dictionary
        df_row['GAME_ID'] = n
        df_row['DATE'] = date
        df_row['AWAY_TEAM'] = away_team
        df_row['AWAY_SCORE'] = away_score
        df_row['HOME_TEAM'] = home_team
        df_row['HOME_SCORE'] = home_score
        df_row['TEAM'] = home_team
        df_row['NUM'] = home_player.find_element(by=By.XPATH, value='./td[1]').text
        df_row['NAME'] = home_player.find_element(by=By.XPATH, value='./th').text
        df_row['GS'] = home_player.find_element(by=By.XPATH, value='./td[2]').text
        df_row['MIN'] = home_player.find_element(by=By.XPATH, value='./td[3]').text
        df_row['FGM'] = home_player.find_element(by=By.XPATH, value='./td[4]').text.split('-')[0]
        df_row['FGA'] = home_player.find_element(by=By.XPATH, value='./td[4]').text.split('-')[1]
        df_row['3PTM'] = home_player.find_element(by=By.XPATH, value='./td[5]').text.split('-')[0]
        df_row['3PTA'] = home_player.find_element(by=By.XPATH, value='./td[5]').text.split('-')[1]
        df_row['FTM'] = home_player.find_element(by=By.XPATH, value='./td[6]').text.split('-')[0]
        df_row['FTA'] = home_player.find_element(by=By.XPATH, value='./td[6]').text.split('-')[1]
        df_row['ORB'] = home_player.find_element(by=By.XPATH, value='./td[7]').text.split('-')[0]
        df_row['DRB'] = home_player.find_element(by=By.XPATH, value='./td[7]').text.split('-')[1]
        df_row['TREB'] = home_player.find_element(by=By.XPATH, value='./td[8]').text
        df_row['PF'] = home_player.find_element(by=By.XPATH, value='./td[9]').text
        df_row['A'] = home_player.find_element(by=By.XPATH, value='./td[10]').text
        df_row['TO'] = home_player.find_element(by=By.XPATH, value='./td[11]').text
        df_row['BLK'] = home_player.find_element(by=By.XPATH, value='./td[12]').text
        df_row['STL'] = home_player.find_element(by=By.XPATH, value='./td[13]').text
        df_row['PTS'] = home_player.find_element(by=By.XPATH, value='./td[14]').text

        df_list.append(df_row) ## append the player row to the df list

    n+=1 ## increment counter for game_id
        
df = pd.DataFrame(df_list) ## create dataframe from list of dictionaries

df.to_pickle(".\data\historical_boxes.pkl") ## save dataframe to pkl in data folder

