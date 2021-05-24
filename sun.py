import pyowm
from datetime import datetime#, timezone
from pytz import timezone

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
owm = pyowm.OWM(os.getenv("OWM_TOKEN"))


def main(*arg):

    mgr = owm.weather_manager()
    obs = mgr.weather_at_place('Budapest,HU')
    w = obs.weather
    #below solution of timezone adjustment doesn't work in docker
    #sunrise = w.sunrise_time(timeformat='date').replace(tzinfo=timezone.utc).astimezone(tz=None)
    sunrise = w.sunrise_time(timeformat='date').astimezone(timezone('Europe/Budapest'))
    sunset = w.sunset_time(timeformat='date').astimezone(timezone('Europe/Budapest'))
    msg = 'Sunrise: %02d:%02d\nSunset: %02d:%02d' % (sunrise.hour, sunrise.minute, sunset.hour, sunset.minute)
    #print(msg)
    bot.send_message(chat_id, text=msg)

if __name__ == "__main__":
    main()

