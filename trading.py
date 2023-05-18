from messages import MESSAGE_TEMPLATE, subAccountName

trixLength = 9
trixSignal = 21

# -- Hyper parameters --
maxOpenPosition = 2
stochOverBought = 0.80
stochOverSold = 0.20
TpPct = 5


def calculate_balances(bitget, dflist):
    usd_balance = bitget.get_balance_of_one_coin('USDT')
    balance_in_usd_per_coin = {}
    for coin in dflist:
        symbol = coin + '/USDT'
        last_price = float(bitget.convert_price_to_precision(
            symbol, bitget.get_bid_ask_price(symbol)['ask']))
        coin_balance = bitget.get_balance_of_one_coin(coin)
        balance_in_usd_per_coin[coin] = coin_balance * last_price
        total_balance_in_usd = sum(
            balance_in_usd_per_coin.values()) + usd_balance
    return usd_balance, balance_in_usd_per_coin, total_balance_in_usd


def calculate_positions(balance_in_usd_per_coin, total_balance_in_usd):
    coin_position_list = []
    for coin in balance_in_usd_per_coin:
        if balance_in_usd_per_coin[coin] > 0.10 * total_balance_in_usd:
            coin_position_list.append(coin)
    return coin_position_list


def buy_condition(row, previousRow=None):
    return row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] <= stochOverBought


def sell_condition(row, previousRow=None):
    return row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] >= stochOverSold


def execute_sells(bitget, coin_position_list, dflist, message_list, open_positions, balance_in_usd_per_coin):
    for coin in coin_position_list:
        symbol = coin + '/USDT'
        sell_price = float(bitget.convert_price_to_precision(
            symbol, bitget.get_bid_ask_price(symbol)['ask']))
        coin_balance = bitget.get_balance_of_one_coin(coin)
        if sell_condition(dflist[coin].iloc[-2], dflist[coin].iloc[-3]):
            open_positions -= 1
            print('sell')
            message_list.append(MESSAGE_TEMPLATE['message_sell'].format(
                subAccountName, str(coin), str(sell_price)))
        else:
            message_list.append(MESSAGE_TEMPLATE['message_keep'].format(subAccountName, str(
                coin_balance), str(coin), str(sell_price), str(balance_in_usd_per_coin[coin])))
            print('keep', coin)
    return message_list, open_positions


def execute_buys(bitget, dflist, message_list, open_positions, coin_position_list, usd_balance):
    if open_positions < maxOpenPosition:
        for coin in dflist:
            if coin not in coin_position_list:
                if buy_condition(dflist[coin].iloc[-2], dflist[coin].iloc[-3]) and open_positions < maxOpenPosition:
                    symbol = coin
                    buy_price = float(bitget.convert_price_to_precision(
                        symbol, bitget.get_bid_ask_price(symbol)['ask']))
                    tp_price = float(bitget.convert_price_to_precision(
                        symbol, buy_price + TpPct * buy_price))
                    buy_quantity_in_usd = bitget.get_balance_of_one_coin(
                        'USDT') * 1 / (maxOpenPosition - open_positions)
                    if open_positions == maxOpenPosition - 1:
                        buy_quantity_in_usd = 0.95 * buy_quantity_in_usd
                    buy_amount = float(bitget.convert_amount_to_precision(symbol, float(
                        bitget.convert_amount_to_precision(symbol, buy_quantity_in_usd / buy_price))))
                    message_list.append(MESSAGE_TEMPLATE['message_buy'].format(
                        subAccountName, str(buy_amount), str(coin), str(buy_price)))
                    print('buy')
                    open_positions += 1
    return message_list, open_positions
