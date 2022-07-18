import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from binance.client import Client
#import models
import talib
import sys
sys.path.append('.')
from sql_alchemy_dir.models import Coin_data, CoinList, session


# from sqlalchemy import select
from sql_alchemy_dir.db_connect import db_con

from utils.date_range import latest_date_in_coin_data, date_tomorrow_in_binance_format
engine = db_con().connect()


load_dotenv()  # take environment variables from .env.
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]


# Variables
client = Client(API_KEY, API_SECRET)


def populate_coin_list():
    symbols = enumerate(client.get_all_tickers())
    for list_id, symbol in symbols:
        coin = CoinList(coin_list_id=list_id, symbol=symbol["symbol"])
        session.merge(coin)
    session.commit()


max_date_in_coin_data = latest_date_in_coin_data()
date_tomorrow = date_tomorrow_in_binance_format()

def populate_coin_data():
    #populate_coin_list()
    date_time_format = "%Y-%m-%d %H:%M:%S"
    # timeframe = "1d"
    # client.KLINE_INTERVAL_1MINUTE = "1d" "1M"
    # timeframes = [
    #     "KLINE_INTERVAL_1MONTH",
    #     "KLINE_INTERVAL_1WEEK",
    #     "KLINE_INTERVAL_3DAY",
    #     "KLINE_INTERVAL_1DAY",
    #     "KLINE_INTERVAL_12HOUR",
    #     "KLINE_INTERVAL_8HOUR",
    #     "KLINE_INTERVAL_6HOUR",
    #     "KLINE_INTERVAL_4HOUR",
    #     "KLINE_INTERVAL_2HOUR",
    #     "KLINE_INTERVAL_1HOUR",
    #     "KLINE_INTERVAL_30MINUTE",
    #     "KLINE_INTERVAL_15MINUTE",
    #     "KLINE_INTERVAL_5MINUTE",
    #     "KLINE_INTERVAL_3MINUTE",
    #     "KLINE_INTERVAL_1MINUTE",
    # ]
    timeframes = [
        "KLINE_INTERVAL_15MINUTE"
    ]

    coin_list = enumerate(
        session.query(CoinList).filter(
            CoinList.symbol.like("%USDT")
        )
    )  # .limit(5))
    for data_id, coin in coin_list:
        coin_name, coin_id = coin.symbol, coin.coin_list_id
        print('******coin_name, coin_id******')
        print(coin_name, coin_id)
        for timeframe in timeframes:
            candlesticks = client.get_historical_klines(
                #coin_name, getattr(Client, timeframe), "18 June, 2022", "06 July, 2022"
                #coin_name, getattr(Client, timeframe), "05 July, 2022", "11 July, 2022"
                coin_name, getattr(Client, timeframe), max_date_in_coin_data, date_tomorrow
            )

            for candlestick in candlesticks:
                (
                    start_date,
                    open_price,
                    high,
                    low,
                    close,
                    volume,
                    end_date,
                    *_other_var,
                ) = candlestick

                start_time = datetime.fromtimestamp(start_date / 1000) #.strftime(date_time_format)
                #start_time = datetime.fromtimestamp(1656979200000 / 1000).strftime(date_time_format)
                end_time = datetime.fromtimestamp(end_date / 1000) #.strftime(date_time_format)
                #now = datetime.now()

                coin_data = Coin_data(
                    coin_data_id=data_id,
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
                    updated_at=datetime.now(),
                )
                session.merge(coin_data)
    session.commit()


#populate_coin_data()

"""
# Solve it with batch challenge
# T1 and T2
# how many days in between
# Then keep adding T1 and T2 until it has reached the original T2
def batch_maker(t1, t2):
    date_format = "%d %b, %Y"
    time_1 = datetime.strptime(t1, date_format)
    time_2 = datetime.strptime(t2, date_format)
    print(time_1)
    print(type(datetime.now()))
    number_of_days = time_2 - time_1
    print(number_of_days.days)
    # date_to_be = '2021 - 09 - 30 00: 00:00'

    f = time_1 + timedelta(days=1 + 1)
    print(f.strftime(date_format))

    date_to_be = []
    for i in range(number_of_days.days):
        f = time_1 + timedelta(days=i + 1)
        date_to_be.append(f.strftime(date_format))
    print(date_to_be)

    date_to_be_1 = [
        (time_1 + timedelta(days=num_of_days_to_add + 1)).strftime(date_format)
        for num_of_days_to_add in range(number_of_days.days)
    ]
    print(date_to_be_1)


# batch_maker("30 Sep, 2021", "09 Oct, 2021")


timeframes = [
    "KLINE_INTERVAL_1MONTH",
    "KLINE_INTERVAL_1WEEK",
    "KLINE_INTERVAL_3DAY",
    "KLINE_INTERVAL_1DAY",
    "KLINE_INTERVAL_12HOUR",
    "KLINE_INTERVAL_8HOUR",
    "KLINE_INTERVAL_6HOUR",
    "KLINE_INTERVAL_4HOUR",
    "KLINE_INTERVAL_2HOUR",
    "KLINE_INTERVAL_1HOUR",
    "KLINE_INTERVAL_30MINUTE",
    "KLINE_INTERVAL_15MINUTE",
    "KLINE_INTERVAL_5MINUTE",
    "KLINE_INTERVAL_3MINUTE",
    "KLINE_INTERVAL_1MINUTE",
]


def batch_maker_2(t_frames, t1, t2):
    import math

    required_number_of_candles = 1000
    number_of_minutes_in_hour = 60
    hours_in_a_day = 24
    days_in_a_week = 7
    days_in_a_month = 30
    minutes_in_a_day = hours_in_a_day * number_of_minutes_in_hour



    length_until_the_digit = len("KLINE_INTERVAL_")

    for t_frame in t_frames:
        if t_frame.endswith("MONTH"):
            print(int(t_frame[length_until_the_digit : -len("MONTH")]), "MONTH")
            print(
                math.ceil(required_number_of_candles / (minutes_in_a_day / (minutes_in_a_day * days_in_a_month * int(t_frame[length_until_the_digit : -len("MONTH")])))))

        elif t_frame.endswith("WEEK"):
            print(int(t_frame[length_until_the_digit : -len("WEEK")]), "WEEK")
            print(
                math.ceil(required_number_of_candles / (minutes_in_a_day / (minutes_in_a_day * days_in_a_week * int(t_frame[length_until_the_digit : -len("WEEK")])))))
        elif t_frame.endswith("DAY"):
            print(int(t_frame[length_until_the_digit : -len("DAY")]), "DAY")
            print(
                math.ceil(required_number_of_candles / (minutes_in_a_day / (minutes_in_a_day * int(t_frame[length_until_the_digit : -len("DAY")])))))
        elif t_frame.endswith("HOUR"):
            print(int(t_frame[length_until_the_digit : -len("HOUR")]), "HOURS")
            print(
                math.ceil(required_number_of_candles / (minutes_in_a_day / (number_of_minutes_in_hour * int(t_frame[length_until_the_digit : -len("HOUR")])))))
        elif t_frame.endswith("MINUTE"):
            print(int(t_frame[length_until_the_digit : -len("MINUTE")]), "MINUTE")
            print(
                math.ceil(required_number_of_candles / (minutes_in_a_day / int(t_frame[length_until_the_digit : -len("MINUTE")]))))

    #         print(t_frame)


batch_maker_2(timeframes, "30 Sep, 2021", "09 Oct, 2021")


"""