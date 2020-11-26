#### this is not a script!
#### for game_id in list_of_game_ids loop is the main www.boardgamegeek.com/xmlapi2/ scraper 
#### add exponential delay for the 429 response



import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import matplotlib.pyplot as plt
#import xml.etree.ElementTree as ET
import lxml
import random
# import urllib



#### collecting general game information: 

rank = []
name = []
geek_rating = []
avg_rating = []
num_voters = []
game_url = []


for page_num in range(1, 199):
    print(page_num)
    page_name = "https://boardgamegeek.com/browse/boardgame/page/" + str(page_num)
    page = requests.get(page_name)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", class_ = "collection_table")
    for row in table.findAll("tr", id = "row_"):
        col = row.findAll("td")
        
        rank.append(int(col[0].get_text()))
        name.append(col[2].find("a").get_text())
        geek_rating.append(float(col[3].get_text()))
        avg_rating.append(float(col[4].get_text()))
        num_voters.append(int(col[5].get_text()))
        game_url.append(col[2].find("a").get("href"))



## dataframe of games (>=30 reviews) ordered by rating

df = pd.DataFrame({"rank" : rank, "name" : name, "geek_rating" : geek_rating, "avg_rating" : avg_rating, 
                   "num_voters" : num_voters, "url" : game_url })






### getting individual user-game ratings from API:



def url_to_xmlsoup(url):
    while True:
        #time.sleep(1)
        game_page = requests.get(url)
        if game_page.status_code == 200:
            break
        elif game_page.status_code == 429:
            
            print("429 waiting on ", url)
            print(game_page.headers)
            #a = int(game_page.headers.get("Retry-After"))
            print("wait", a)
            #time.sleep(a)
            
        else:
            
            print(game_page.status_code)
            time.sleep(2 + random.randint(0,1))
            print("waiting on", url)
    return BeautifulSoup(game_page.content, "lxml")




list_of_game_ids = list(df.game_id)

comments = []
game_properties = {}
game_properties_list = []

game = []
user = []
user_rating = []


#############
#############

for game_id in list_of_game_ids:    
    
    url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + str(game_id) + "&stats=1"
    soup = url_to_xmlsoup(url)
        
    print("game_id:", game_id)
    
    
    #game type
    game_properties["id"] = game_id
    game_properties["family"] = soup.find(type="family").get("name")
    game_properties["category"] = [x.get("value") for x in list(soup.find_all(type = "boardgamecategory"))]
    game_properties["mechanics"] = [x.get("value") for x in list(soup.find_all(type = "boardgamemechanic"))]
    game_properties_list.append(game_properties)
    
    num_ratings = int(soup.find("usersrated").get("value"))
    print(num_ratings)
    #game ratings page by page:
    
    for pg_num in range(1, int(num_ratings/100) + 2):
        url = "https://www.boardgamegeek.com/xmlapi2/thing?id=" + str(game_id) +"&ratingcomments=1"+ "&page=" + str(pg_num)
        soup = url_to_xmlsoup(url)
        
        
        
        

    
        comments = soup.find_all("comment")
        for x in comments:
            game.append(game_id)
            user.append(x.get("username"))
            user_rating.append(x.get("rating"))



