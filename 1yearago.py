import csv
from datetime import date

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
daylio = os.getenv("DAYLIO_PATH") #wherever you saved your daylio_export.csv file on your computer

def main():
    today = date.today()
    y = str(int(today.strftime("%Y"))-1)
    y += "-" + today.strftime("%m-%d")
    entries = []
    with open(os.path.join(os.path.dirname(__file__),daylio), encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            elif row[0] == y:
                entries.append(row[6])
            line_count += 1
    # We have to reverse the order of entries of that day for them to be in correct chronological order
    entries.reverse()
    msg = '*1 year ago today:*\n\n'
    msg += "\n\n".join(entries)
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
    main()
