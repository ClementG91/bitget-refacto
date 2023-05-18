from spot_bitget import SpotBitget

def configure_bitget(account_to_select, secret, production=False):
    bitget = SpotBitget(
        apiKey=secret[account_to_select]["apiKey"],
        secret=secret[account_to_select]["secret"],
        password=secret[account_to_select]["password"],
    )
    return bitget
