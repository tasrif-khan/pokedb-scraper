import time
import pandas as pd
import numpy as np
import random as random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Creates an window of Chrome that Selenium will use. Need to download chromedriver from internet.
driver = webdriver.Chrome(executable_path="C:\\Users\\tasri\\Documents\\chromedriver.exe")

# Navigate to where we want to start
driver.get("https://pokemondb.net/pokedex/bulbasaur")

# Method for scraping the page
def poke_info_grabber(variation):
    time.sleep(random.random())

    # Lets get the pokemon name and ID   
    id = driver.find_element('xpath',f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[1]/td').text
    name = driver.find_element('xpath','//*[@id="main"]/h1').text

    # Some pokemon have alternate forms so if they are of an alternate variation we will get that name from the tab.
    if variation > 1:
        name = driver.find_element('xpath', f'/html/body/main/div[3]/div[1]/a[{variation}]').text

    # Adding those two to our lists
    poke_id.append(id)
    poke_name.append(name)

    # Grab URL from current pokemon page
    poke_url.append(driver.current_url)

    # Get elements of the pokemon types, abilities and egg types.
    type_holders = driver.find_elements('xpath',f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[2]/td/a')
    abilities_holders = driver.find_elements('xpath',f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[6]/td/span/a')
    egg_holders = driver.find_elements('xpath', f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[3]/div/div[2]/table/tbody/tr[1]/td/a')
    
    # Get hidden abilities if they are avalible and then adding it to the list
    try:
        hidden_ability = driver.find_element('xpath', f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[2]/table/tbody/tr[6]/td/small/a').text
    except Exception:
        hidden_ability = 'none'  
    hidden_abilities.append(hidden_ability) 
      
    # Getting the egg cycle or the amount of steps needed to hatch the egg for this Pokemon.
    egg_time = driver.find_element('xpath', f'/html/body/main/div[3]/div[2]/div[{variation}]/div[1]/div[3]/div/div[2]/table/tbody/tr[3]/td').text
    egg_time = egg_time[0:3]
    egg_cycles.append(egg_time)
    
    # Getting the text from the selenium element and then adding a none placeholder if it doesnt have the second type.
    type_list = [item.text.lower().capitalize() for item in type_holders]
    type_list.extend(["none"] * (2 - len(type_holders)))
    types.append(type_list)

    abilities_list = [item.text for item in abilities_holders]
    abilities_list.extend(["none"] * (2 - len(abilities_holders)))
    abilities.append(abilities_list)

    egg_list = [item.text for item in egg_holders]
    egg_list.extend(["none"] * (2 - len(egg_holders)))
    egg_group.append(egg_list)

# End of Method

# Set up pokedex lists
poke_id = []
poke_name = []
poke_url = []
types = []
abilities = []
hidden_abilities = []
egg_group = []
egg_cycles = []

# Main body

for i in range(904):

    # Starting off with the default version of the Pokemon
    variation = 1

    # Invoke our scraper method
    poke_info_grabber(variation)
    
    # While loop to check for any alternate forms of this Pokemon
    while variation > 0:
        try:
            variation += 1
            # If we find an alternate form element we will click on that and invoke the scraper again.
            driver.find_element('xpath',f'/html/body/main/div[3]/div[1]/a[{variation}]').click()
            poke_info_grabber(variation)   
        except Exception:
            # Breaking the loop to go to the next page
            variation = 0
            pass

    
    # Click to the next Pokemon
    driver.find_element('xpath','/html/body/main/nav[1]/a[contains(@class,"entity-nav-next")]').click()

# All the data we collected.
lists = [poke_id, poke_name, poke_url, types, abilities, hidden_abilities, egg_group, egg_cycles]

# Turn all the lists into dataframes, then concatenate the dataframes into a final, large dataframe.
pokedex_matrix = pd.concat([pd.DataFrame(i) for i in lists], axis = 1)

# Giving each column a name
pokedex_matrix.columns = ["id", "name", "url", "type1", "type2", "ability1", "abilitiy2", "hiddenability", "egggroup1", "egggroup2", "eggcycles"]

# Print the table to see if anything is wrong
print(pokedex_matrix)

# Exporting it to a path on your computer as a CSV
pokedex_matrix.to_csv('C:\\Users\\tasri\\Desktop\\pokemon_db.csv')