import pandas
import plotly.graph_objects as go

import sys
sys.path.append('.')


dataframes = {}

distinct_symbol_sql = "SELECT DISTINCT(symbol) FROM coin_data"
distinct_symbol_df = pandas.read_sql(distinct_symbol_sql, "sqlite:///C:\\Github\\coinPrice\\Coin_price.db")
#symbol = 'BTCUSDT'
for symbol in distinct_symbol_df['symbol']:

    #sql = "SELECT * FROM coin_data WHERE symbol = '{}' LIMIT 700".format(symbol)
    sql = '''
    WITH DESC_TIME_CANDLES AS 
    (SELECT open_time, symbol, open, high, low, close, volume 
    FROM coin_data
    WHERE symbol = '{}'
    ORDER BY coin_data_id, coin_list_id, symbol, open_time DESC
    LIMIT 200)
    SELECT open_time, symbol, open, high, low, close, volume
    FROM DESC_TIME_CANDLES
    ORDER BY symbol, open_time
    '''.format(symbol)

    df = pandas.read_sql(sql, "sqlite:///C:\\Github\\coinPrice\\Coin_price.db")

    if not df.empty:
        #print(symbol, 'in if not df.empty')

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
            print("{} is coming out the squeeze".format(symbol))

    # save all dataframes to a dictionary
    # we can chart individual names below by calling the chart() function

#     dataframes[symbol] = df
#
#
# def chart(df):
#     candlestick = go.Candlestick(x=df['open_time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])
#     upper_band = go.Scatter(x=df['open_time'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
#     lower_band = go.Scatter(x=df['open_time'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})
#
#     upper_keltner = go.Scatter(x=df['open_time'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'blue'})
#     lower_keltner = go.Scatter(x=df['open_time'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'blue'})
#
#     fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner])
#     fig.layout.xaxis.type = 'category'
#     fig.layout.xaxis.rangeslider.visible = False
#     fig.show()
#
#
# df_1 = dataframes['BTCUSDT']
# chart(df_1)
