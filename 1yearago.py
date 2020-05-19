import csv
from datetime import date

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

today = date.today()
y = str(int(today.strftime("%Y"))-1)
y += "-" + today.strftime("%m-%d")

entries = []
#with open("daylio_export.csv", encoding="utf8") as csv_file:
with open(os.path.join(os.path.dirname(__file__),"daylio_export.csv"), encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
            #print(f'Column names are {", ".join(row)}')
        elif row[0] == y:
            #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            entries.append(row[6])
        line_count += 1
    #print(f'Processed {line_count} lines.')

# WE have to reverse the order of entries of that day for them to be in correct chronological order
entries.reverse()

msg = '*1 year ago today:*\n\n'
msg += "\n\n".join(entries)


bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)




