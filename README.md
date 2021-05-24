# Python Telegram Bot

This is my Python Telegram bot, that I run inside a Docker Container on a Raspberry Pi.

The python files can be called from the command line as well as through Telegram via the status_bot.py file, including arguments.

## Example usage:

Command CLI: `python rate.py 8eur 3000huf 12eur`

Command Telegram: `\rate 8eur 3000huf 12eur`

Response:

```
€8.0 = 2783Ft
3000Ft = €8.62
€12.0 = 4174Ft
```

Command CLI: `python fuel.py`

Command Telegram: `python fuel.py`

Response:

```
Benzin: €1.519, 528Ft
Diesel: €1.329, 462Ft
```
