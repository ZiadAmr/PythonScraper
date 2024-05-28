from selenium import webdriver
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests 

date_format = '%Y-%m-%dT%H:%M:%S.000Z'

# checks if a twitter url is valid by submitting a request to that address
def is_valid_twitter_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print(f"Received unexpected status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error while checking the URL: {e}")
        return False
    
# checks if ticker starts with a $ followed by a 3 or 4 letter word
def validate_ticker(ticker):
    if ticker[0] != "$":
        return False
    elif len(ticker) < 4 or len(ticker) > 5:
        return False
    elif not ticker[1:].isalpha():
        return False
    else:
        return True


# returns number of occurances of `tag` in `url` using `browser` during time period `t`
def getOccurances(tag, url, browser, t):
    browser.get(url)

    last_height = browser.execute_script("return document.body.scrollHeight")

    current_dateTime = datetime.now()
    counter = 0
    while True:

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        tweets = soup.find_all('article', {"data-testid":"tweet"})

        for tweet in tweets:
            if tag.lower() in tweet.get_text().lower():
                timestamp_tag = tweet.find('time')
                date_obj = datetime.strptime(timestamp_tag["datetime"], date_format)
                timedelta = current_dateTime - date_obj
                if timedelta.total_seconds() / 60 < t:
                    counter += 1

        # Scroll down to the bottom
        browser.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        
        # Wait to load the page
        time.sleep(4)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return counter

    
browser = webdriver.Firefox()

urls = []
print("input 10 urls:")
for i in range(10):
    twitter_url = str(input())
    if not is_valid_twitter_url(twitter_url):
        print("Invalid Twitter Url")
        exit()
    urls.append(twitter_url)

ticker = str(input("Input the cashtag: "))
if not validate_ticker(ticker):
    print("Invalid Cashtag")
    exit()

time_interval = int(input("Input the time interval: "))

total = 0
for url in urls:
    total += getOccurances(ticker, url, browser, time_interval)

print(ticker, "has been mentioned", total ,"times in the last", time_interval, "minutes")
# print("$SPX has been mentioned", getOccurances("$SPX", "https://twitter.com/Mr_Derivatives", browser, 60*24*30), "times in the last 30 mins ")
browser.close()