import json
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

URL = "https://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity"

driver.get(URL)

soup = BeautifulSoup(driver.page_source, features="html.parser")

tags = soup.findAll('tr')

genres = [tag.contents[2].string for tag in tags]

with open('all_genres.json', 'w') as write_file:
    json.dump(genres, write_file)
