
import requests as req

class CExchange():

    def __init__(self, coin_from, coin_to, fee):
        
        self.__coin_from = coin_from
        self.__coin_to = coin_to
        self.__fee = fee

    def coef(self):

        ticker_from = self.__coin_from.ticker()
        ticker_to = self.__coin_to.ticker()
        url = "https://api.cryptonator.com/api/ticker/%s-%s" % (ticker_from, ticker_to)

        result = req.get(url)
        result_json = result.json()
        coef = float(result_json["ticker"]["price"])

        return coef

    def __call__(self, account_from, account_to, amount):

        if not (account_from.check_coin(self.__coin_from) and account_to.check_coin(self.__coin_to)):

            raise ValueError("Bad accounts for coin")

        main_account_from = self.__coin_from.account()
        main_account_to = self.__coin_to.account()
        amount_from = amount + self.__fee
        amount_to = amount * self.coef()

        if account_from.balance() < amount_from or main_account_to.balance() < amount_to:

            raise ValueError("Bad balance")

        account_from.move(main_account_from, amount_from)
        main_account_to.move(account_to, amount_to)

