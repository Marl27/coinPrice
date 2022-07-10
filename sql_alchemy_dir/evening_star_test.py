import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from binance.client import Client
import models
import talib
import numpy as np
import pandas as pd
import sqlite3
# from sqlalchemy import select

from db_connect import db_con

coin_list = models.session.query(models.Coin_data_ta_lib).filter(models.Coin_data.symbol == 'BTCUSDT').filter(
    models.Coin_data.interval_id == 'KLINE_INTERVAL_1DAY').order_by(models.Coin_data.open_time)
"""
coin_list = models.session.query(models.Coin_data_ta_lib).filter(models.Coin_data.symbol == 'BTCUSDT').filter(
    models.Coin_data.interval_id == 'KLINE_INTERVAL_1DAY').order_by(models.Coin_data.open_time)


print("8888888888888888888")
print(coin_list)
print(type(coin_list))
list_of_data = []
for coin in coin_list:
    # print(coin.__dict__)
    coin_data = {
        "coin_data_id": coin.coin_data_id,
        "coin_list_id": coin.coin_list_id,
        "symbol": coin.symbol,
        "interval_id": coin.interval_id,
        "open_time": coin.open_time,
        "open": coin.open,
        "high": coin.high,
        "low": coin.low,
        "close": coin.close,
        "volume": coin.volume,
        "close_time": coin.close_time
    }
    list_of_data.append(coin_data)

    #
    # np_coin_data = {
    #     "coin_data_id": np.array(coin.coin_data_id),
    #     "coin_list_id": np.array(coin.coin_list_id),
    #     "symbol": np.array(coin.symbol),
    #     "interval_id": np.array(coin.interval_id),
    #     "open_time": np.array(coin.open_time),
    #     "open": np.array(coin.open, dtype='f'),
    #     "high": np.array(coin.high, dtype='f'),
    #     "low": np.array(coin.low, dtype='f'),
    #     "close": np.array(coin.close, dtype='f'),
    #     "volume": np.array(coin.volume),
    #     "close_time": np.array(coin.close_time)
    # }
    # integer = talib.CDLEVENINGSTAR(np_coin_data['open'], np_coin_data['high'], np_coin_data['low'], np_coin_data['close'], penetration=0)
    # print(integer)

print(list_of_data)
"""
# df = pd.read_sql_query('SELECT * FROM Coin_data_ta_lib’, con=db_con)

sql_query = pd.read_sql('''
                        SELECT * 
                        FROM coin_data_ta_lib 
                        WHERE symbol='XRPUSDT'
                        AND interval_id = 'KLINE_INTERVAL_1DAY'
                        --ORDER BY open_time
                        ''', con=db_con())
df = pd.DataFrame(sql_query, columns=
[#'coin_data_id',
 #'coin_list_id',
 'symbol',
 'interval_id',
 'open_time',
 'open',
 'high',
 'low',
 'close'])
 #'volume',
 #'close_time'])

print(sql_query)

evening_start = talib.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close'], penetration=0)
morning_star = talib.CDLMORNINGDOJISTAR(df['open'], df['high'], df['low'], df['close'], penetration=0)

three_black_crows = talib.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])
abandoned_baby = talib.CDLABANDONEDBABY(df['open'], df['high'], df['low'], df['close'], penetration=0)

doji = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
trendLine = talib.HT_TRENDLINE(df['close'])

print('trendLine')
print(trendLine)

print("****morning_star****")
print(morning_star[morning_star != 0])
print(df.loc[[312, 1044]])
# print(df.loc[[2132]])

print('**')
print("****evening_start****")
print(evening_start[evening_start != 0])
print(df.loc[[105, 132, 837, 864, 1701]])
#print(df.loc[[955]])

print('**')
print("****three_black_crows****")
print(three_black_crows[three_black_crows != 0])

print('**')
print("****abandoned_baby****")
print(abandoned_baby[abandoned_baby != 0])

print('**')
print("****doji****")
print(doji[doji != 0])
