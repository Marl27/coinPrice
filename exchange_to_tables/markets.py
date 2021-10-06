import os

from binance.client import Client
from sql_alchemy_dir import models

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]


# Variables
client = Client(API_KEY, API_SECRET)


def populate_coin_list():
    symbols = client.get_all_tickers()
    count = 0
    for symbol in symbols:
        count += 1
        coin = models.CoinList(coin_list_id=count, symbol=f"{symbol['symbol']}")
        # coin = models.CoinList(symbol=f"{symbol['symbol']}")
        # models.session.add(coin)
        models.session.merge(coin)
        models.session.commit()
        # print(symbol)


def populate_coin_data():
    pass


populate_coin_list()
