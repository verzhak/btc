
from abc import ABC, abstractmethod
from collections import namedtuple

SBalance = namedtuple("SBalance", [ "deposite", "holded", "unconfirmed" ])
STransaction = namedtuple("STransaction", [ "address", "category", "amount", "confirmations", "txid", "fee", "time" ])

class CAccount(ABC):

    @abstractmethod
    def balance(self): pass

    @abstractmethod
    def name(self): pass

    @abstractmethod
    def addresses(self): pass

    @abstractmethod
    def create_address(self): pass

    @abstractmethod
    def move(self, account, amount): pass

    @abstractmethod
    def send(self, addr, amount): pass

    @abstractmethod
    def transactions(self, count = None, _from = None): pass

class CCoin(ABC):

    @abstractmethod
    def rpc(self): pass

    @abstractmethod
    def ticker(self): pass

    @abstractmethod
    def account(self, account_name = ""): pass

