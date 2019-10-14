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
import smtplib
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            }


def check_price(URL):
    """
    function that creates the page and returns the current price
    :return: the current price as a float
    """
    # returns all the data from the URL provided
    page = requests.get(URL, headers = headers)

    # issues along the line if I use just one soup. I use two so that the soup find method will not return NoneType
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # from amazon, grab the span productTitle which corresponds to the title of the item
    # .get_text = get rid of span tags
    # .strip() = return only non-whitespace string
    title = soup2.find(id = "productTitle").get_text().strip()

    # price is either priceblock_saleprice or priceblock_ourprice
    price = soup2.find(id = "priceblock_ourprice")
    if price is None:
        price = soup2.find(id = "priceblock_saleprice").get_text()
    else:
        price = price.get_text()

    """
        print(converted_price, "\n")
        print(title)

        if converted_price < 150:
            send_mail()
    """

    converted_price = convert_price(price)
    return converted_price




def convert_price(price_str):
    """
    Changes the price string of form "CDN$   131.99" into just 131.99 as an integer
    :param price_str: the price from the page
    :return: int price
    """
    first_digit = 0
    for i in range(len(price_str)):
        if price_str[i].isdigit():
            first_digit = i
            break

    converted_price = float(price_str[first_digit:])
    return converted_price


def send_mail(email, password, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Command sent by email server to identify itself, to start process of sending email
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, password)

    subject = 'Price has lowered for one of your items'
    body = 'Check the amazon link %s' % url

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(email, email, msg)

    print("Email has successfully been sent")

    server.quit()


def get_info():

    email = input("Email: ")
    password = input("Email password: ")
    url = input("Amazon URL: ")
    current_price = check_price(url)
    max_price = input("Current price is " + str(current_price) + ". What is your maximum price? ")

    return email, password, url, max_price


def main():
    # TODO: User input to get URL and email
    email, password, url, max_price = get_info()

    print(email, password, url, max_price)

    while check_price(url) > max_price:
        time.sleep(60 * 60)
    print("Price has dropped!")
    send_mail(email, password, url)
    # check_price()


if __name__ == '__main__':
    main()