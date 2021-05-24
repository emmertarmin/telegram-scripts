from requests import get
from datetime import datetime, timezone
from pytz import timezone



import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
logs = "db/logs.txt"

def requester(url):
    try:
        return get(url).json()
    except Exception as e:     # most generic exception you can catch
        with open(logs, 'a+', encoding="utf-8") as f:
            f.write(str(datetime.now().isoformat()) + ": " + str(e) + "\n")
        return False
    finally:
        pass

# Main function returns basic info about next race
def main(*arg):
    obj = requester('http://ergast.com/api/f1/current/next.json')
    if obj:
        #ssn = obj["MRData"]["RaceTable"]["Races"][0]["season"]
        #rnd = obj["MRData"]["RaceTable"]["Races"][0]["round"]
        date = obj["MRData"]["RaceTable"]["Races"][0]["date"]
        time = obj["MRData"]["RaceTable"]["Races"][0]["time"]
        dt = datetime.strptime(date + time[:-1] + " +0000", '%Y-%m-%d%H:%M:%S %z')
        dt = dt.astimezone(timezone('Europe/Budapest'))
        time = str(dt.time())
        locality = obj["MRData"]["RaceTable"]["Races"][0]["Circuit"]["Location"]["locality"]
        country = obj["MRData"]["RaceTable"]["Races"][0]["Circuit"]["Location"]["country"]
        msg = "Upcoming race:\n\n*" + locality + ", " + country + "*\n" + date + " " + time
    else:
        msg = "Request failed"
    # Only include interactive part of message if it's the bot itself sending this info
    if __name__ != "__main__":
        msg += "\n\n/f1last . /f1stand . f1next"
    #print(msg)
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

# Results of last race
def f1last(*arg):
    obj = requester('https://ergast.com/api/f1/current/last/results.json')
    if obj:
        ssn = obj["MRData"]["RaceTable"]["season"]
        rnd = obj["MRData"]["RaceTable"]["round"]
        racename = obj["MRData"]["RaceTable"]["Races"][0]["raceName"]
        msg = "*" + racename + " Results*\n" + ssn + "/" + rnd + "\n\n"
        res = obj["MRData"]["RaceTable"]["Races"][0]["Results"]
        msg += "```"
    else:
        msg = "Request failed"
    for i in range(len(res)):
        if int(res[i]["position"])<10:
            msg += " "
        msg += res[i]["position"] + " | "
        if res[i]["points"] != '0':
            msg += res[i]["points"] + " "
        msg += res[i]["Driver"]["familyName"] + " "
        if "Time" in res[i]:
            msg += res[i]["Time"]["time"]
        if res[i]["status"] != "Finished":
            msg += res[i]["status"]
        msg += "\n"
    msg += "```"
    # Only include interactive part of message if it's the bot itself sending this info
    if __name__ != "__main__":
        msg += "\nf1last . /f1stand . /f1next"
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
	
# Current standing in championship
def f1stand(*arg):
    obj = requester('https://ergast.com/api/f1/current/driverStandings.json')
    if obj:
        ssn = obj["MRData"]["StandingsTable"]["StandingsLists"][0]["season"]
        rnd = obj["MRData"]["StandingsTable"]["StandingsLists"][0]["round"]
        msg = "*Driver Standings*\n" + ssn + "/" + rnd + "\n\n"
        dst = obj["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
        msg += "```"
        for i in range(len(dst)):
            if int(dst[i]["position"])<10:
                msg += " "
            msg += dst[i]["position"] + " | "
            msg += dst[i]["Driver"]["code"] + " "
            p = "   " + dst[i]["points"]
            msg += p[-3:] + " "
            msg += dst[i]["Constructors"][0]["name"] + "\n"
        msg += "```"
    else:
        msg = "Request failed"
    # Only include interactive part of message if it's the bot itself sending this info
    if __name__ != "__main__":
        msg += "\n/f1last . f1stand . /f1next"
    bot.send_message(chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
    main()
