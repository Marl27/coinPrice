import pytest
from sql_alchemy_dir import models

def test_non_pushed_assets_are_non_assests():
    coin_list = models.session.query(models.CoinList).all()
    assert False

"""
query to find out the symbols which are present in coin_list but not in coin_data
###################################################################################

SELECT 
		cl.symbol as coin_list_symbol
FROM coin_list cl
WHERE cl.symbol like "%USDT"
AND cl.symbol not in (SELECT cd.symbol as coin_data_symbol FROM coin_data cd)

###################################################################################

SELECT 
cl.symbol as coin_list_symbol, cd.symbol as coin_data_symbol
FROM coin_list cl 
LEFT JOIN  coin_data cd
	ON cl.coin_list_id = cd.coin_list_id 
WHERE cl.symbol like "%USDT"
AND cd.symbol is null
ORDER BY cl.symbol;
"""