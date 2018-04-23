
from enum import Enum

from .btc import CBTC
from .ltc import CLTC
from .dash import CDash

class ECoin(Enum):

    BTC = 1 # Bitcoin
    LTC = 2 # Litecoin
    Dash = 3 # Litecoin
    MONERO = 4 # Monero

def get_coin_by_ind(ind):

    if ind == ECoin.BTC:

        return CBTC

    elif ind == ECoin.LTC:

        return CLTC

    elif ind == ECoin.Dash:

        return CDash
    
    elif ind == ECoin.MONERO:

        raise Exception("Not implemented")

    raise Exception("Bad coin")

def get_coin_by_ticker(name):

    if name == "BTC":

        return CBTC

    elif name == "LTC":

        return CLTC

    elif name == "Dash":

        return CDash
    
    elif name == "Monero":

        raise Exception("Not implemented")

    raise Exception("Bad coin")

