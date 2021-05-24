import json
from requests import get
import random


import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Let's keep track of past comics sent in this xkcd.db file. It has to be created once
db = os.path.join(os.path.dirname(__file__),"db/xkcd.db")

# Helper function tells whether comic has been sent before
def xkcd_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if str(title) in line:
                return True
    return False

def main(*arg):
    obj = get('https://xkcd.com/info.0.json').json()
    num = obj["num"]
    if not xkcd_is_in_db(num):
        img_url = obj["img"]
        #print(obj["safe_title"])
        bot.send_message(chat_id, text="#" + str(num) + "*: " + obj["safe_title"])
        bot.send_photo(chat_id=chat_id, photo=img_url)
        bot.send_message(chat_id, text=obj["alt"])
    else:
        last = num
        # I desperately want to avoid getting in an infinite loop while checking for unsent xkcd files, so I'll just simply give up at the hundredth try.
        for i in range(100):
            num = random.randint(0, last)
            if not xkcd_is_in_db(num):
                break
        obj = get('https://xkcd.com/' + str(num) + '/info.0.json').json()
        img_url = obj["img"]
        #print(obj["safe_title"])
        bot.send_message(chat_id, text="#" + str(num) + ": " + obj["safe_title"])
        bot.send_photo(chat_id=chat_id, photo=img_url)
        bot.send_message(chat_id, text=obj["alt"])
    with open(db, 'a+') as f:
        if not xkcd_is_in_db(num):
            f.write(str(num) + "\n")


if __name__ == "__main__":
    main()