# coinPrice

- Activate venv
- install requirements
- run strategy - python sql_alchemy_dir/evening_star_test.py
- run DB code - python sql_alchemy_dir/push_to_db.py


New data is currently pushed into coin_data_ta_lib

Yet to work out a working strategy using candlestick patterns


#### Current working status
- running - python sql_alchemy_dir/push_to_db.py 
- gets candlestick data FROM MAX(open_time) in the table TILL tomorrow.
 