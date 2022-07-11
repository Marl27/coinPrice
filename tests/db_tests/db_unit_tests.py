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