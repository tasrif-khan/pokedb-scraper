# Import all the necessary tools needed for scraping
import time
import pandas as pd
import numpy as np
import random as random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import requests

# Need to download Chrome webdriver, then install it into PATH.
# This creates an instance of Chrome that we can control using Selenium
driver = webdriver.Chrome(executable_path="C:\\Users\\tasri\\Documents\\chromedriver.exe")

# Navigate to where we want to start
driver.get("https://pokemondb.net/pokedex/bulbasaur")

def poke_info_grabber(variation):
    time.sleep(2.5)   

    name = driver.find_element('xpath','//*[@id="main"]/h1').text

    if variation > 1:
        name = driver.find_element('xpath', f'/html/body/main/div[3]/div[1]/a[{variation}]').text

    
    # Get elements of both abilities and types
    type_links = driver.find_elements('xpath',f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[2]/td/a')
    abilities_links = driver.find_elements('xpath',f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[6]/td/span[1]/a')
    # Get hidden abilities
    try:
        hidden_ability = driver.find_element('xpath', f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[6]/td/small/a').text
    except Exception:
        hidden_ability = 'none'
    hidden_abilities.append(hidden_ability)    
    
    # Grab URL from current pokemon page
    poke_name.append(name)
    poke_url.append(driver.current_url)
    
    # Some pokemon have alternate forms - we want to ignore those for now.
    type_list = [i.text.lower() for i in type_links]
    type_list.extend(["none"] * (2 - len(type_links)))
    types.append(type_list)

    abilities_list = [i.text.lower() for i in abilities_links]
    abilities_list.extend(["none"] * (2 - len(abilities_links)))
    abilities.append(abilities_list)



# Set up pokedex lists
poke_name = []
poke_url = []
types = []
abilities = []
hidden_abilities = []
egg_group = []
egg_cycles = []


for i in range(8):
    variation = 1
    poke_info_grabber(variation)
    
    while variation > 0:
        try:
            variation += 1
            driver.find_element('xpath',f'/html/body/main/div[3]/div[1]/a[{variation}]').click()
            poke_info_grabber(variation)   
        except Exception:
            variation = 0
            pass

    
    # Click to the next page
    driver.find_element('xpath','/html/body/main/nav[1]/a[contains(@class,"entity-nav-next")]').click()

# All the data we collected.
lists = [poke_name, poke_url, types, abilities, hidden_abilities]

# Turn all the lists into dataframes, then concatenate the dataframes into a final, large dataframe.
pokedex_matrix = pd.concat([pd.DataFrame(i) for i in lists], axis = 1)

# Give the columns of our dataframe some proper names
pokedex_matrix.columns = ["name", "url", "type1", "type2", "ability1", "abilitiy2", "hiddenability"]
#pokedex_matrix.columns = ["name", "type1", "type2", "ability1", "ability2", "ability3",
#                   "pokedex_entry", "hp","attack","defence","sp_attack","sp_defence", "speed"]
print(pokedex_matrix)