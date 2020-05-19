

import pyowm
from datetime import datetime, timezone

import os
import telegram
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")
owm = pyowm.OWM(os.getenv("OWM_TOKEN"))


def sun():
    if not owm.is_API_online():
        bot.send_message(chat_id, text='OWM is offline')
        return
    observation = owm.weather_at_place('Budapest,HU')
    w = observation.get_weather()
    sunrise = w.get_sunrise_time(timeformat='date').replace(tzinfo=timezone.utc).astimezone(tz=None)
    sunset = w.get_sunset_time(timeformat='date').replace(tzinfo=timezone.utc).astimezone(tz=None)
    msg = 'Sunrise: %02d:%02d\nSunset: %02d:%02d' % (sunrise.hour, sunrise.minute, sunset.hour, sunset.minute)
    bot.send_message(chat_id, text=msg)

sun()

