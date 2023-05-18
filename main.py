from datetime import datetime
from config import load_secret
from bitget import configure_bitget
from data import calculate_indicators, load_historical_data
from trading import (
    calculate_balances,
    calculate_positions,
    execute_sells,
    execute_buys,
)
import discord
from discord_utils import send_messages_to_discord
from messages import MESSAGE_TEMPLATE, subAccountName


# Timeframe to use for technical analysis
timeframe = "1h"

# -- Variables for indicators --
trixLength = 9
trixSignal = 21
stochOverBought = 0.80
stochOverSold = 0.20


def get_time_now():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time


def main():
    # Initialize bitget API client
    secret = load_secret("secret.json")
    bitget = configure_bitget("bitget_exemple", secret, production=True)

    # Initialize Discord client
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    client = discord.Client(intents=intents)

    # Define your list of coins
    pairlist = [
        "BTC/USDT:USDT",
        "ETH/USDT:USDT",
        "BNB/USDT:USDT",
        "XRP/USDT:USDT",
        "SOL/USDT:USDT",
        "SHIB/USDT:USDT",
        "CHZ/USDT:USDT",
        "DOGE/USDT:USDT",
        "MATIC/USDT:USDT",
        "AVAX/USDT:USDT",
    ]

    # Load historical data
    message_list = []
    dflist = load_historical_data(
        bitget, pairlist, timeframe, 1000, message_list
    )

    # Calculate indicators
    dflist = calculate_indicators(dflist, trixLength, trixSignal)

    # Calculate balances
    usd_balance, balance_in_usd_per_coin, total_balance_in_usd = calculate_balances(
        bitget, dflist
    )
    # Calculate positions
    coin_position_list = calculate_positions(
        balance_in_usd_per_coin, usd_balance
    )

    # Execute sales if sell condition is met
    open_positions = len(coin_position_list)
    message_list, open_positions = execute_sells(
        bitget,
        coin_position_list,
        dflist,
        message_list,
        open_positions,
        balance_in_usd_per_coin,
    )

    # Execute buys if buy condition is met
    message_list, open_positions = execute_buys(
        bitget,
        dflist,
        message_list,
        open_positions,
        coin_position_list,
        usd_balance,
    )
    message_list.append(
        MESSAGE_TEMPLATE["message_wallet"].format(
            subAccountName, str(total_balance_in_usd)
        )
    )
    # Send messages to Discord
    send_messages_to_discord(client, secret, message_list)


if __name__ == "__main__":
    main()
