import os
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client
from sql_alchemy_dir import models

#from sqlalchemy import select
from sql_alchemy_dir.db_connect import db_con


engine = db_con().connect()


load_dotenv()  # take environment variables from .env.
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']


# Variables
client = Client(API_KEY, API_SECRET)


def populate_coin_list():
    symbols = enumerate(client.get_all_tickers())
    for list_id, symbol in symbols:
        coin = models.CoinList(coin_list_id=list_id, symbol=symbol['symbol'])
        models.session.merge(coin)
    models.session.commit()


def populate_coin_data():
    populate_coin_list()
    date_time_format = '%d-%m-%Y %H:%M:%S'
    timeframe = "1d"
    interval = Client.KLINE_INTERVAL_1DAY

    coin_list = enumerate(models.session.query(models.CoinList).filter(models.CoinList.symbol.like('%USDT')).limit(5))
    for data_id, coin in coin_list:
        coin_name, coin_id = coin.symbol, coin.coin_list_id
        candlesticks = client.get_historical_klines(
            coin_name, interval, "27 Sep, 2021", "28 Sep, 2021"
        )
        print(interval)
        for candlestick in candlesticks:
            start_date, open_price, high, low, close, volume, end_date, *_other_varr = candlestick
            start_time = datetime.fromtimestamp(start_date/1000).strftime(date_time_format)
            end_time = datetime.fromtimestamp(end_date/1000).strftime(date_time_format)
            coin_data = models.Coin_data(coin_data_id=data_id,
                                         coin_list_id=coin_id,
                                         symbol=coin_name,
                                         interval_id=timeframe,
                                         open_time=start_time,
                                         open=open_price,
                                         high=high,
                                         low=low,
                                         close=close,
                                         volume=volume,
                                         close_time=end_time,
                                         )
            models.session.merge(coin_data)
    models.session.commit()


populate_coin_data()


#commit just once first-go - 3:47.59
#commit just once second-go - 3:50.59

#commit twice first-go - 3:50.59
#commit twice second-go - 3:30.59

#commit within the loop first-go - 5:46.59
#commit within the loop second-go - 3:30.59

