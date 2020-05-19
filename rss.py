import feedparser
import time
from bs4 import BeautifulSoup
from IPython.display import Image
import json


import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")



db = os.path.join(os.path.dirname(__file__),"feeds.db")
limit = 24 * 3600 * 1000

current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title has been in database for a time defined in "limit"
# for limit=24*3600*1000, posts from last 24 hours will return "false"
def post_is_in_db_with_old_timestamp(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                ts_as_string = line.split('|', 1)[1]
                ts = int(ts_as_string)
                if current_timestamp > ts + limit:
                    return True
    return False

def clean(unclean):
    cleaned = "".join([x for x in unclean if 32 <= ord(x) <= 126 or 160 <= ord(x) <= 255])
    return cleaned

def esc(s):
    output = ""
    for letter in s:
        if letter == "*" or letter == "_":
            output += "\\" + letter
        else:
            output += letter
    return output


def reddit(url):
    for key in url:
        feed = feedparser.parse(url[key])
        posts_to_print = []


        for entry in feed.entries[:5]:
            title = clean(entry.title)
            if post_is_in_db_with_old_timestamp(title):
                continue
            posts_to_print.append(title)
            content = BeautifulSoup(entry.content[0].value, "lxml")
            if content.find('td'):
                td = content.table.findAll(name='td')[1]
                link = td.findAll(name='a')[1]['href']
                if link[-3:] != 'jpg':
                    continue
                print(title)
                """
                img = Image(link,width=300)
                display(img)
                """



def podcast(url):
    for key in url:
        msg = ''
        feed = feedparser.parse(url[key])
        if ('title' not in feed.channel or 'channel' not in feed): #Check if feed loads at all
            msg += (key + " failed to load\n")

        else: #If loads properly, do all the rest
            channel_title = feed.channel.title
            
            posts_to_print = []
            
            for item in feed.entries:
                # if post is already in the database, skip it
                title = clean(item.title)
                if post_is_in_db_with_old_timestamp(title):
                    continue
                posts_to_print.append(title)
                desc = BeautifulSoup(item.description, "lxml")
                if desc.find('p'):
                    desc = desc.findAll('p')[0].get_text()
                else:
                    desc = desc.get_text()
                desc = esc(desc)
                #Some of the RSS feeds I'm tracking are not like the others, so now I need to correct fot that
                msg += chr(187) + ' ' + '*' + channel_title + '* '
                if key in ['Beyond Victory','Reply All','Waveform','The Hacker Factor Blog']:
                    desc = desc.partition('\n')[0]
                if key == 'Darknet Diaries':
                    desc = desc.split('.')[0] + '.'
                if key in ['TWiSt']:
                    title = ''
                else:
                    title += '\n'
                if key in ['No Dumb Questions']:
                    desc = ''
                else:
                    desc += '\n'
                msg += chr(187) + ' ' + title + desc
                # TODO: images maybe
                """
                img = Image(desc.findAll('p')[1].img['src'], width=200)
                display(img)
                """
        if msg != '':
            #print(msg)
            bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

        with open(db, 'a+') as f:
            for title in posts_to_print:
                title.rstrip()
                if not post_is_in_db(title):
                    f.write(title + "|" + str(current_timestamp) + "\n")

url = {}

url["reddit"] = {
    "MechanicalKeyboards":"https://reddit.com/r/MechanicalKeyboards/top.rss?sort=top&t=week",
    "CustomKeyboards":"https://reddit.com/r/CustomKeyboards/top.rss?sort=top&t=week"
}

url["podcast"] = json.loads(os.getenv("PODCAST_RSS_URL"))

def main():
    #reddit(url['reddit'])
    podcast(url['podcast'])

if __name__ == "__main__":
    main()




