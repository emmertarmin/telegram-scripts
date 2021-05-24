# Python Telegram Bot

This is my Python Telegram bot, that I run inside a Docker Container on a Raspberry Pi.

The python files can be called from the command line as well as through Telegram via the `status_bot.py` file, including arguments. [See examples](#example-usage).

Before running it the first time, you need to fill `.env-example` with your own tokens, rename it to `.env`, and create the `db` folder with a few empty files inside. More on this [here](#setting-up-the-project).

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
## Setting up the project

You'll have to create a `db` folder with database files (empty text files). The folder structure looks approximately like this:

```
|   .dockerignore
|   .env
|   covid.py
|   docker-compose.yml
|   Dockerfile
|   f1.py
|   fuel.py
|   rate.py
|   requirements.txt
|   status_bot.py
|   sun.py
|   xkcd.py
|   
+---db
|       fuel.db
|       logs.txt
|       rate.db
|       xkcd.db
```