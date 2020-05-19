from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import json
from requests import get

import time

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")



#disable the loading of images
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')




def main():
    driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=r'C:/Users/User/geckodriver')
    driver.get('https://www.blinkist.com/en/nc/daily')
    #time.sleep(5)

    title = driver.find_elements_by_class_name('daily-book__headline')[0].get_attribute('innerHTML')
    synopsis = driver.find_elements_by_class_name('book-tabs__content-inner')[0].get_attribute('innerHTML')
    synopsis = BeautifulSoup(synopsis, "lxml").text
    duration = driver.find_elements_by_class_name('book-stats__label')[0].get_attribute('innerHTML')
    author = driver.find_elements_by_class_name('daily-book__author')[0].get_attribute('innerHTML')
    msg = 'Today on Blinkist:\n\n'
    msg += '*' + ' '.join(title.split()) + '*\n'
    msg += ' '.join(author.split()) + '\n'
    msg += synopsis
    msg += '\nwww.blinkist.com/en/nc/daily'
    driver.quit()
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)


if __name__ == "__main__":
    main()

