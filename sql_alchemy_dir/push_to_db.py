import os
from datetime import datetime

from binance.client import Client
from sql_alchemy_dir import models

from sqlalchemy import select
from sql_alchemy_dir.db_connect import db_con
#import db_connect

engine = db_con().connect()


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']


# Variables
client = Client(API_KEY, API_SECRET)


def populate_coin_list():
    symbols = client.get_all_tickers()
    count = 0
    for symbol in symbols:
        count += 1
        coin = models.CoinList(coin_list_id=count, symbol=f"{symbol['symbol']}")
        models.session.merge(coin)
        models.session.commit()


def populate_coin_data():
    populate_coin_list()
    date_time_format = '%d-%m-%Y %H:%M:%S'
    timeframe = "1d"
    count = 0

    coin_list = models.session.query(models.CoinList).all()
    for coin in coin_list:
        count += 1
        coin_name = coin.symbol
        if coin_name.endswith("USDT"):
            print(coin_name)

            candlesticks = client.get_historical_klines(
                coin_name, Client.KLINE_INTERVAL_1DAY, "27 Sep, 2021", "27 Sep, 2021"
            )
            print(Client.KLINE_INTERVAL_1DAY)
            for candlestick in candlesticks:
                start_time = str(datetime.fromtimestamp(candlestick[0]/1000).strftime(date_time_format))
                end_time = str(datetime.fromtimestamp(candlestick[6]/1000).strftime(date_time_format))
                coin_data = models.Coin_data(coin_data_id=count,
                                             symbol=coin_name,
                                             interval_id= timeframe,
                                             open_time = start_time,
                                             open= candlestick[1],
                                             high = candlestick[2],
                                             low = candlestick[3],
                                             close = candlestick[4],
                                             volume = candlestick[5],
                                             close_time = end_time,
                                             )
                models.session.merge(coin_data)
                models.session.commit()

populate_coin_data()



