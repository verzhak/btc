
from .btc import CBTC
from .btc import CBTCAccount

class CLTCAccount(CBTCAccount): pass

class CLTC(CBTC):

    ticker = lambda self: "LTC"

