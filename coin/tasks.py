
from django.db import transaction
from celery import shared_task

from . import models
from .models import Account, Address, Currency, Transaction, Exchange

@shared_task
@transaction.atomic
def refresh_user(user_name):

    account_name = user_name

    for currency in Currency.objects.all():

        refresh_account(currency, account_name)

@shared_task
@transaction.atomic
def refresh_account(currency, account_name):

    if type(currency) == str:

        currency = Currency.objects.get(label = currency)

    obj = currency.get_obj().account(account_name)
    balance = obj.balance()

    try:

        account = Account.objects.select_for_update().get(currency = currency, name = account_name)
        account.balance = balance
        account.save()

    except Account.DoesNotExist:

        account = Account.objects.create(currency = currency, name = account_name, balance = balance)
        obj = account.get_obj()

    for addr in obj.addresses():

        Address.objects.select_for_update().get_or_create(account = account, address = addr)

    for tx in obj.transactions():

        Transaction.objects.update_or_create(
                account = account,
                address = tx.address,
                category = tx.category,
                amount = tx.amount,
                txid = tx.txid,
                fee = tx.fee,
                time = tx.time, defaults = dict(confirmations = tx.confirmations))

@shared_task
def send(label, account_name, address, amount):

    currency = Currency.objects.filter(label = label).first()
    account = Account.objects.filter(currency = currency, name = account_name).first()
    obj = account.get_obj()

    try:

        obj.send(address, amount)
        refresh_account(currency, account_name)

    except ValueError as err:

        return err.args

    return None

@shared_task
def create_address(label, account_name):

    currency = Currency.objects.filter(label = label).first()
    account = Account.objects.filter(currency = currency, name = account_name).first()
    obj = account.get_obj()

    address = obj.create_address()
    refresh_account(currency, account_name)

    return address

@shared_task
def exchange(_id, account_name, amount):

    exchange = Exchange.objects.filter(id = _id).first()
    account_from = Account.objects.filter(currency = exchange.currency_from, name = account_name).first()
    account_to = Account.objects.filter(currency = exchange.currency_to, name = account_name).first()

    exchange_obj = exchange.get_obj()
    account_from_obj = account_from.get_obj()
    account_to_obj = account_to.get_obj()

    try:

        exchange_obj(account_from_obj, account_to_obj, amount)
        refresh_account(exchange.currency_from, account_name)
        refresh_account(exchange.currency_to, account_name)

    except ValueError as err:
    
        return err.args
            
    return None

