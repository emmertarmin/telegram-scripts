import csv
import requests

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def csv_to_array(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    for line in lines[1:]: # skip first line (has headers)
        el = [i.strip() for i in line.split(',')]
        yield el # don't return, that immediately ends the function


def main(*args):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = csv_to_array(url)

    population = {'Hungary':9773000, 'Germany':83020000, 'Austria':8859000}

    msg = "*COVID*\n"

    for row in data:
        # already split on commas.
        for country in population:
            if (row[1] == country):
                row = row[-8:]
                diff = 0
                for i in range(len(row[1:])):
                    diff = diff + int(row[i+1]) - int(row[i])
                msg += country + ': *'
                msg += str(round(diff/population[country]*100000)) + '*\n'
            
    msg += '... per 100\'000 during the last 7 days'
    #print(msg)
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)



if __name__ == "__main__":
    main()