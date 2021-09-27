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
        #print(symbol)

def populate_coin_data():
    print("starting - populate_coin_data()")
    #populate_coin_list()
    date_time_format = '%d-%m-%Y %H:%M:%S'

    coin_list = models.session.query(models.CoinList).all()
    for coin in coin_list:
        #print(coin.symbol)
        coin_name = coin.symbol
        if coin_name.endswith("USDT"):
            #print("TRUE")
            print(coin_name)

            candlesticks = client.get_historical_klines(
                coin_name, Client.KLINE_INTERVAL_1DAY, "25 Sep, 2021", "27 Sep, 2021"
            )
            for candlestick in candlesticks:
                print("%d -- %d" % (candlestick[0]/1000, candlestick[6]/1000))
                start_time = str(datetime.fromtimestamp(candlestick[0]/1000).strftime(date_time_format))
                end_time = str(datetime.fromtimestamp(candlestick[6]/1000).strftime(date_time_format))
                print("%s -- %s" % (start_time, end_time))
                print(candlestick)
    #coin_data = models.Coin_data(coin_list_id=count, symbol=f"{symbol['symbol']}")


'''
    __tablename__ = 'coin_data'
    coin_data_id = Column(Integer, primary_key=True)
    symbol = Column(String(10)) #TEXT [pk, not null, unique]
    interval_id = Column(String(10)) #int [pk, not null]
    open_time = Column(String(20)) #TEXT [pk, not null]
    open = Column(String(20)) #NUMERIC(18,9)
    high = Column(String(20)) #NUMERIC(18,9)
    low = Column(String(20)) #NUMERIC(18,9)
    close = Column(String(20)) #NUMERIC(18,9)
    volume = Column(String(20)) #TEXT
    close_time = Column(String(20)) #TEXT
'''
populate_coin_data()


#populate_coin_list()
