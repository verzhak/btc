
from .btc import CBTC
from .btc import CBTCAccount

class CDashAccount(CBTCAccount): pass

class CDash(CBTC):

    ticker = lambda self: "Dash"

