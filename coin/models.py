
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from coin_api import get_coin_by_ticker
from coin_api.base import STransaction
from coin_api.exchange import CExchange

class Currency(models.Model):

    label = models.CharField(_("Label"), max_length = 20, default = "", primary_key = True)
    ticker = models.CharField(_("Ticker"), max_length = 4, default = "")
    host = models.CharField(_("Hostname"), default = "", max_length = 100, blank = True, null = True)

    __str__ = lambda self: self.label
    get_obj = lambda self: get_coin_by_ticker(self.ticker)(self.host)

    class Meta:

        verbose_name_plural = _("currencies")

class Account(models.Model):

    currency = models.ForeignKey(Currency)
    name = models.CharField(_("Account name"), default = "", max_length = 100)
    balance = models.FloatField(_("Balance"), validators = [ MinValueValidator(0) ])

    get_obj = lambda self: self.currency.get_obj().account(self.name)

    class Meta:

        verbose_name_plural = _("accounts")
        unique_together = ("currency", "name")

class Address(models.Model):

    account = models.ForeignKey(Account)
    address = models.CharField(_("Address"), default = "", max_length = 100)

    class Meta:

        verbose_name_plural = _("addresses")

class Transaction(models.Model):

    account = models.ForeignKey(Account)
    address = models.CharField(_("Address"), default = "", max_length = 100)
    category = models.CharField(_("category"), default = "", max_length = 100)
    txid = models.CharField(_("txid"), default = "", max_length = 100)
    time = models.CharField(_("time"), default = "", max_length = 100)
    amount = models.FloatField(_("Amount"), validators = [ MinValueValidator(0) ], default = 0)
    fee = models.FloatField(_("Fee"), validators = [ MinValueValidator(0) ], default = 0)
    confirmations = models.PositiveIntegerField(_("Confirmations"), default = 0)

    get_obj = lambda self: STransaction(
        address = self.address,
        category = self.category,
        amount = self.amount,
        confirmations = self.confirmations,
        txid = self.txid,
        fee = self.fee,
        time = self.time)

    class Meta:

        verbose_name_plural = _("transactions")
        unique_together = ("account", "category", "txid")

class Exchange(models.Model):

    label = models.CharField(_("Label"), max_length = 100, default = "", unique = True)
    currency_from = models.ForeignKey(Currency, related_name = "Currency_from", default = None)
    currency_to = models.ForeignKey(Currency, related_name = "Currency_to", default = None)
    # coef = models.FloatField(_("Coefficient"), validators = [ MinValueValidator(0.000001) ], default = 1)
    fee = models.FloatField(_("Fee"), validators = [ MinValueValidator(0) ], default = 0)

    __str__ = lambda self: "%s <-> %s" % (self.currency_from.label, self.currency_to.label)
    # get_obj = lambda self: CExchange(self.currency_from.get_obj(), self.currency_to.get_obj(), self.coef, self.fee) # TODO
    get_obj = lambda self: CExchange(self.currency_from.get_obj(), self.currency_to.get_obj(), self.fee)

    class Meta:

        verbose_name_plural = _("exchanges")

