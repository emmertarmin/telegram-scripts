import json
import requests
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import os
from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(os.getenv("TELEGRAM_BOT_ID"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# my own python files and functions
import covid
import daylio # My python file that tells me what I wrote in my daylio calendar a year ago. Remove if not needed
import f1
import fuel
import rate
import rss # My python file that fetches podcast and blog updates. Remove if not needed
import sun
import xkcd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def help(update, context):
    """Send a message when the command /help is issued."""
    msg = ""
    msg += "\n/covid 7-Day-Incident per Million"
    msg += "\n/daylio What did I do a year ago today?"
    msg += "\n/f1last Results of the last race"
    msg += "\n/f1stand Driver standings"
    msg += "\n/f1next Time and place of the next race"
    msg += "\n/fuel prices and consump. (args: Xeur Ykm)"
    msg += "\n/ip Outside ip address"
    msg += "\n/rate Exchange rates (args: Xeur/Yhuf)"
    msg += "\n/rss check rss feeds for new content"
    msg += "\n/sun Time of sunrise and sunset"
    msg += "\n/xkcd Sends last comic image and alt"
    msg.rstrip()
    update.message.reply_text(msg)

            
def ip(update, context):
    ip = requests.get('https://api.ipify.org').text
    msg = 'public IP: ' + ip
    update.message.reply_text(msg)


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv("TELEGRAM_BOT_ID"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("covid", covid.main))
    dp.add_handler(CommandHandler("daylio", daylio.main))
    dp.add_handler(CommandHandler("f1last", f1.f1last))
    dp.add_handler(CommandHandler("f1stand", f1.f1stand))
    dp.add_handler(CommandHandler("f1next", f1.main))
    dp.add_handler(CommandHandler("fuel", fuel.main))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ip", ip))
    dp.add_handler(CommandHandler("rate", rate.main))
    dp.add_handler(CommandHandler("rss", rss.main))
    dp.add_handler(CommandHandler("sun", sun.main))
    dp.add_handler(CommandHandler("xkcd", xkcd.main))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=0.0)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()




