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
TANKERKOENIG_API_KEY = os.getenv("TANKERKOENIG_API_KEY")
TANKERKOENIG_LOCATION = os.getenv("TANKERKOENIG_LOCATION")
logs = "db/logs.txt"
db = "db/fuel.db"
import rate

# links:
# petrol stations:
# https://creativecommons.tankerkoenig.de/json/list.php?lat=52.5069296&lng=13.1438708&rad=4&sort=price&type=diesel&apikey=TANKERKOENIG_API_KEY
# prices:
# https://creativecommons.tankerkoenig.de/json/detail.php?id=TANKERKOENIG_LOCATION&apikey=TANKERKOENIG_API_KEY

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

    eurhuf = rate.eurhuf()["huf"]

    e5 = 0
    e10 = 0
    diesel = 0
    # if we have it cached today, don't make a request
    with open(db, 'r', encoding="utf-8") as f:
        for line in f:
            if t[:10] in line:
                e5, e10, diesel = [float(i) for i in line.split("|")[1:]]
                break
    # otherwise we make the request
    if e5 > 0 and e10 > 0 and diesel > 0:
        pass
    else:
        obj = requester('https://creativecommons.tankerkoenig.de/json/detail.php?id=' + TANKERKOENIG_LOCATION + '&apikey=' + TANKERKOENIG_API_KEY)
        if not obj:
            msg = "Request failed"
            return
        e5 = obj["station"]["e5"]
        e10 = obj["station"]["e10"]
        diesel = obj["station"]["diesel"]
        with open(db, 'a+', encoding="utf-8") as f:
            f.write("|".join([t, str(e5), str(e10), str(diesel)]) + "\n")

    dist = 0
    cost = 0
    display_rates = True
    arguments = sys.argv
    if hasattr(context, 'args'):
        arguments = context.args
    for arg in arguments:
        if "km" in arg and dist == 0:
            dist = float(arg[:-2])
        if "eur" in arg and cost == 0:
            cost = float(arg.split("eur")[0])
    if dist > 0 and cost > 0:
        display_rates = False
        consumption1 = (cost/e5) / (dist/100)
        consumption2 = (cost/diesel) / (dist/100)
        msg += "Eq. consumption:\n"
        msg += "*" + str(round(consumption1, 1)) + "*L/100km Benzin\n"
        msg += "*" + str(round(consumption2, 1)) + "*L/100km Diesel\n\n"

    if display_rates:
        msg += "```\n"
        msg += "Benzin: €" + str(e5) + ", " + str(int(e5*eurhuf)) + "Ft\n"
        msg += "Diesel: €" + str(diesel) + ", " + str(int(diesel*eurhuf)) + "Ft\n"
        msg += "```"

    #print(msg)
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)


if __name__ == "__main__":
    main()
