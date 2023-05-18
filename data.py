from ta import trend, momentum
from messages import MESSAGE_TEMPLATE, subAccountName


def calculate_indicators(dflist, trixLength, trixSignal):
    for coin in dflist:
        df = dflist[coin]
        df.drop(columns=df.columns.difference(
            ['open', 'high', 'low', 'close', 'volume']), inplace=True)
        df['TRIX'] = trend.ema_indicator(
            trend.ema_indicator(trend.ema_indicator(
                close=df['close'], window=trixLength), window=trixLength),
            window=trixLength
        )
        df['TRIX_PCT'] = df["TRIX"].pct_change() * 100
        df['TRIX_SIGNAL'] = trend.sma_indicator(
            df['TRIX_PCT'], window=trixSignal)
        df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']
        df['STOCH_RSI'] = momentum.stochrsi(
            close=df['close'], window=14, smooth1=3, smooth2=3)
        df['RSI'] = momentum.rsi(close=df['close'], window=14)
        df.dropna(inplace=True)
    return dflist


def load_historical_data(bitget, pairlist, timeframe, nbOfCandles, message_list=None):
    dflist = {}
    for pair in pairlist:
        try:
            df = bitget.get_more_last_historical_async(pair, timeframe, 1000)
            dflist[pair.replace('/USDT:USDT', '')] = df
        except Exception as err:
            if message_list is not None:
                print(err)
                message_list.append(MESSAGE_TEMPLATE['message_erreur'].format(
                    subAccountName, nbOfCandles, pair))
    return dflist
