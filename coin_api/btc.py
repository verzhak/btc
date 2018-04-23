
import datetime
import jsonrpclib

from .base import CCoin, CAccount, STransaction

class CBTCAccount(CAccount):

    def __init__(self, coin, name):

        self.__coin = coin
        self.__name = name

        self.__coin.rpc().getaccountaddress(self.__name)

    balance = lambda self: self.__coin.rpc().getbalance(self.__name)
    name = lambda self: self.__name
    addresses = lambda self: self.__coin.rpc().getaddressesbyaccount(self.__name)
    create_address = lambda self: self.__coin.rpc().getnewaddress(self.__name)
    check_coin = lambda self, coin: (type(coin) == type(self.__coin))

    def move(self, account, amount):

        if self.balance() < amount:

            raise ValueError("Too many coin")

        if not self.__coin.rpc().move(self.__name, account.name(), amount):

            raise ValueError("Some error")

    def send(self, addr, amount):

        try:
            
            txid = self.__coin.rpc().sendfrom(self.__name, addr, amount)

        except jsonrpclib.jsonrpc.ProtocolError as err:

            raise ValueError("Bad amount")

        return txid

    def transactions(self, count = None, _from = None):

        if count is None:

            txs = self.__coin.rpc().listtransactions(self.__name)

        elif _from is None:

            txs = self.__coin.rpc().listtransactions(self.__name, count)

        else:

            txs = self.__coin.rpc().listtransactions(self.__name, count, _from)

        result = []

        for t in txs:

            if t["category"] == "move":

                address = ""
                confirmations = 0
                txid = "move_%d" % t["time"]
                fee = 0

            else:

                address = t["address"]
                confirmations = t["confirmations"]
                txid = t["txid"]

                if t["category"] == "send":

                    fee = t["fee"]

                else:

                    fee = 0

            transaction = STransaction(
                address = address,
                category = t["category"],
                amount = float(t["amount"]),
                confirmations = int(confirmations),
                txid = txid,
                fee = float(fee),
                time = datetime.datetime.fromtimestamp(t["time"]).strftime("%d.%m.%Y %H:%M:%S"))

            result.append(transaction)

        return result

class CBTC(CCoin):

    def __init__(self, host):
        
        self.__rpc = jsonrpclib.ServerProxy(host)

    rpc = lambda self: self.__rpc
    ticker = lambda self: "BTC"

    def account(self, account_name = ""):

        return CBTCAccount(self, account_name)

