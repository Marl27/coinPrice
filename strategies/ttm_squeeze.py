import pandas
import plotly.graph_objects as go

import sys
sys.path.append('.')


def get_coin_data_from_table():
    distinct_symbol_sql = "SELECT DISTINCT(symbol) FROM coin_data"
    distinct_symbol_df = pandas.read_sql(distinct_symbol_sql, "sqlite:///C:\\Github\\coinPrice\\Coin_price.db")
    #symbols = ['AUDUSDT', 'SHIBUSDT', 'BTTCUSDT']
    symbol_to_trade_list = []
    # for symbol in symbols:
    for symbol in distinct_symbol_df['symbol']:
        #print(symbol)
        sql = '''
        WITH DESC_TIME_CANDLES AS 
        (SELECT open_time, symbol, open, high, low, close, volume 
        FROM coin_data
        WHERE symbol = '{}'
        --AND open_time < '2022-07-17 19:00:00.000000'
        ORDER BY coin_data_id, coin_list_id, symbol, open_time DESC
        LIMIT 500)
        SELECT open_time, symbol, open, high, low, close, volume
        FROM DESC_TIME_CANDLES
        ORDER BY symbol, open_time
        '''.format(symbol)

        df = pandas.read_sql(sql, "sqlite:///C:\\Github\\coinPrice\\Coin_price.db")
        symbol_to_trade = ttm_squeeze_strategy(df, symbol)
        if symbol_to_trade is not None:
            symbol_to_trade_list.append(symbol_to_trade)
        # chart(data_frame)

        # TODO Implement a function to push symbol_to_trade to DB table
        # TODO for strategy testing. containing the following:-
        # TODO symbol_to_trade, datetime for when it was identified.
    return symbol_to_trade_list


def ttm_squeeze_strategy(df, symbol):
    if not df.empty:

        df['20sma'] = df['close'].rolling(window=20).mean()
        df['stddev'] = df['close'].rolling(window=20).std()
        df['lower_band'] = df['20sma'] - (2 * df['stddev'])
        df['upper_band'] = df['20sma'] + (2 * df['stddev'])

        df['TR'] = abs(df['open'].astype(float) - df['low'].astype(float))
        df['ATR'] = df['TR'].rolling(window=20).mean()

        df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
        df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

        def in_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

        df['squeeze_on'] = df.apply(in_squeeze, axis=1)

        if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
            element = str("{} is coming out the squeeze".format(symbol))
            print(element)
            return element

def chart(df):
    candlestick = go.Candlestick(x=df['open_time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])
    upper_band = go.Scatter(x=df['open_time'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
    lower_band = go.Scatter(x=df['open_time'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})

    upper_keltner = go.Scatter(x=df['open_time'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'blue'})
    lower_keltner = go.Scatter(x=df['open_time'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'blue'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()

#get_coin_data_from_table()
