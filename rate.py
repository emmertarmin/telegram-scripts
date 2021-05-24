from requests import get
from datetime import datetime, timezone
from pytz import timezone

import os
import sys
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
EXCHANGERATES_ACCESS_KEY = os.getenv("EXCHANGERATES_ACCESS_KEY")
logs = "db/logs.txt"
db = "db/rate.db"

# links:
# Exchange rate
# http://api.exchangeratesapi.io/v1/latest?access_key=EXCHANGERATES_ACCESS_KEY&base=EUR&symbols=USD,HUF

def requester(url):
    try:
        return get(url).json()
    except Exception as e:     # most generic exception you can catch
        with open(logs, 'a+', encoding="utf-8") as f:
            f.write(str(datetime.now().isoformat()) + ": " + str(e) + "\n")
        return False
    finally:
        pass

def main(update = {}, context = {}):
    msg = ""
    now = datetime.now()
    now.astimezone(timezone('Europe/Budapest'))
    t = now.strftime('%Y-%m-%dT%H:%M:%S')

    rates = eurhuf()

    exch_eur = 0
    exch_huf = 0
    display_rates = True
    arguments = sys.argv
    if hasattr(context, 'args'):
        arguments = context.args
    for arg in arguments:
        if "eur" in arg:
            display_rates = False
            exch_eur = float(arg.split("eur")[0])
            exch_huf = exch_eur*rates["huf"]
            msg += "*€" + str(round(exch_eur, 2)) + "* = " + str(int(exch_huf)) + "Ft\n"
        if "huf" in arg:
            display_rates = False
            exch_huf = int(arg.split("huf")[0])
            exch_eur = exch_huf/rates["huf"]
            msg += "*" + str(int(exch_huf)) + "Ft* = €" + str(round(exch_eur, 2)) + "\n"
    if display_rates:
        msg += "\n"
        msg += "*1 EUR = * " + str(int(rates["huf"])) + " HUF\n"
        msg += "*1 USD = * " + str(int(rates["huf"]/rates["usd"])) + " HUF\n"
        msg += "*1 CHF = * " + str(int(rates["huf"]/rates["chf"])) + " HUF\n"
        msg += "*1 GBP = * " + str(int(rates["huf"]/rates["gbp"])) + " HUF\n"

    #print(msg)
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

def eurhuf():
    now = datetime.now()
    now.astimezone(timezone('Europe/Budapest'))
    t = now.strftime('%Y-%m-%dT%H:%M:%S')

    huf = 0
    usd = 0
    chf = 0
    gbp = 0
    # if we have it cached today, don't make a request
    with open(db, 'r', encoding="utf-8") as f:
        for line in f:
            if t[:10] in line:
                huf, usd, chf, gbp = [float(i) for i in line.split("|")[1:]]
                break
    # otherwise we make the request
    if huf > 0 and usd > 0 and chf > 0 and gbp > 0:
        pass
    else:
        print("REQUESTING!!!!!!!!!!!!!!")
        obj = requester('http://api.exchangeratesapi.io/v1/latest?access_key=' + EXCHANGERATES_ACCESS_KEY + '&base=EUR&symbols=USD,HUF,CHF,GBP')
        if not obj:
            print("Request failed")
            return
        huf = float(obj["rates"]["HUF"])
        usd = float(obj["rates"]["USD"])
        chf = float(obj["rates"]["CHF"])
        gbp = float(obj["rates"]["GBP"])
        with open(db, 'a+', encoding="utf-8") as f:
            f.write("|".join([t, str(huf), str(usd), str(chf), str(gbp)]) + "\n")
    return {"huf":huf, "usd":usd, "chf":chf, "gbp":gbp}
if __name__ == "__main__":
    main()
