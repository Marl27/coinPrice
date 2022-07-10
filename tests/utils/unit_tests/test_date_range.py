import pytest
import datetime as dt
from datetime import datetime, timedelta
from utils.date_range import date_7_days_ago, binance_API_date_format, latest_date_in_coin_data, date_tomorrow_in_binance_format

@pytest.mark.parametrize("expected",
                         [(str(dt.date.today() - dt.timedelta(days=7))),])
def test_date_7_days_ago(expected):
    assert date_7_days_ago() == expected

@pytest.mark.parametrize("input, expected",
                         [(date_7_days_ago(), datetime.strptime(date_7_days_ago(), '%Y-%m-%d').strftime("%d %b, %Y")),
                          ('2022-07-10', '10 Jul, 2022'), ])
def test_binance_API_date_format(input, expected): # , yyyy_mm_dd):
    assert binance_API_date_format(input) == expected
    # return datetime.strptime(yyyy_mm_dd, '%Y-%m-%d').strftime("%d %b, %Y")

# def test_latest_date_in_coin_data():
#     # Worked at first, suddenly stopped working
#     # engine = db_con().connect()
#     # result_proxy = engine.execute("SELECT MAX(open_time) FROM coin_data WHERE symbol = 'BTCUSDT';")
#     # test, *more_test = result_proxy
#
#     fingers_crossed = models.session.query(func.max(models.Coin_data.open_time)).filter_by(symbol='BTCUSDT')
#
#     result, *unpacking_rest_of_the_tuple = fingers_crossed
#     #result = None
#     if result:
#         print('in IF')
#
#         #result, *unpacking_rest_of_the_tuple = result_proxy
#         latest_date_in_the_table = str(result[0]).split(' ')
#         date_in_right_format = binance_API_date_format(latest_date_in_the_table[0])
#     else:
#         print('else')
#         date_in_right_format = binance_API_date_format(date_7_days_ago())
#
#     return date_in_right_format
#
# #print(latest_date_in_coin_data())
#
# def test_date_tomorrow_in_binance_format():
#     return binance_API_date_format(str(dt.date.today() + dt.timedelta(days=1)))
#
