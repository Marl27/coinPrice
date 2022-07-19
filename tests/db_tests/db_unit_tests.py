from sqlalchemy import func
import sys
sys.path.append('.')
from sql_alchemy_dir import models

def test_number_of_15_mins_from_startdate_to_lastdate():
    max_date_for_btcusdt = models.session.query(func.max(models.Coin_data.open_time)).filter_by(symbol='BTCUSDT')
    result, *unpacking_rest_of_the_tuple = max_date_for_btcusdt


test_number_of_15_mins_from_startdate_to_lastdate()
def test_coin_data_id_matches_with_the_symbol():
    pass

# sql = '''
#         WITH DESC_TIME_CANDLES AS
#         (SELECT open_time, symbol, open, high, low, close, volume
#         FROM coin_data
#         WHERE symbol = '{}'
#         AND open_time < '2022-07-17 19:00:00.000000'
#         ORDER BY coin_data_id, coin_list_id, symbol, open_time DESC
#         LIMIT 500)
#         SELECT open_time, symbol, open, high, low, close, volume
#         FROM DESC_TIME_CANDLES
#         ORDER BY symbol, open_time
#         '''.format(symbol)
#
#         df = pandas.read_sql(sql, "sqlite:///C:\\Github\\coinPrice\\Coin_price.db")
