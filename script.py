from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

browser = webdriver.Firefox()
browser.get('https://twitter.com/Mr_Derivatives')

SCROLL_PAUSE_TIME = 2
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(browser.page_source, 'html.parser')
tweets = soup.find_all('div', {"data-testid":"tweetText"})

tweet_data = []
for tweet in tweets:
    if "$TSLA" in tweet.get_text():
        tweet_data.append(tweet.get_text())

print(tweet_data)