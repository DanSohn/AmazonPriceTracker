"""
A quick project where I can get a url from an amazon page, and then given credentials and a price range,
it will email the user when the item falls under the price range
Things to do:
Get information from amazon page
Get user's information
Send email
Do I want it running every hour? Do I need to write a script to have it turned on when computer turns on
In email, sending the url as a link, not just as a string
"""

import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.ca/Mattress-Underblanket-Controller-Settings-Auto-Off/dp/B07G85QKK7/ref=sr_1_7?keywords=electric+blanket&qid=1570827364&sr=8-7"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}

# returns all the data from the URL provided
page = requests.get(URL, headers = headers)

# issues along the line if I use just one soup. I use two so that the soup find method will not return NoneType
soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

# from amazon, grab the span productTitle which corresponds to the title of the item
# .get_text = get rid of span tags
# .strip() = return only non-whitespace string
title = soup2.find(id = "productTitle").get_text().strip()
#title = title.get_text()
#title = title.strip()

price = soup2.find(id = "priceblock_saleprice").get_text().strip()
print(price, "\n")
print(title)