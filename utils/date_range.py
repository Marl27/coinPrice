from datetime import datetime, timedelta
import datetime as dt
from sqlalchemy import func
import sys
sys.path.append('.')
from sql_alchemy_dir import models
#from sql_alchemy_dir.db_connect import db_con

##start_time
#00:08
#00:19



def date_7_days_ago():
    return str(dt.date.today() - dt.timedelta(days=7)) #str(week_ago)

def binance_API_date_format(yyyy_mm_dd):
    return datetime.strptime(yyyy_mm_dd, '%Y-%m-%d').strftime("%d %b, %Y")

def latest_date_in_coin_data():
    # Worked at first, suddenly stopped working
    # engine = db_con().connect()
    # result_proxy = engine.execute("SELECT MAX(open_time) FROM coin_data WHERE symbol = 'BTCUSDT';")
    # test, *more_test = result_proxy

    max_date_for_btcusdt = models.session.query(func.max(models.Coin_data.open_time)).filter_by(symbol='BTCUSDT')

    result, *unpacking_rest_of_the_tuple = max_date_for_btcusdt
    #result = None
    if result:
        print('in IF')

        #result, *unpacking_rest_of_the_tuple = result_proxy
        latest_date_in_the_table = str(result[0]).split(' ')
        date_in_right_format = binance_API_date_format(latest_date_in_the_table[0])
    else:
        print('else')
        date_in_right_format = binance_API_date_format(date_7_days_ago())

    return date_in_right_format

#print(latest_date_in_coin_data())

def date_tomorrow_in_binance_format():
    return binance_API_date_format(str(dt.date.today() + dt.timedelta(days=1)))

