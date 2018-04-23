
import json
from django import forms
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.template import loader

from . import tasks
from lib import LoginRequiredMixin
from .models import Currency, Account, Transaction, Address, Exchange

class WalletView(LoginRequiredMixin, ListView):

    template_name = "wallets.html"

    def get_queryset(self):
        
        # TODO А зачем вообще тогда celery?
        tasks.refresh_user.apply_async(args = [ str(self.request.user) ]).wait()
        
        return Account.objects.filter(name = self.request.user).order_by("currency")

class AccountView(LoginRequiredMixin, ListView):

    template_name = "account.html"

    def get_context_data(self, **kwargs):

        label = self.kwargs["label"]
        currency = get_object_or_404(Currency, label = label)
        account = get_object_or_404(Account, currency = currency, name = self.request.user)

        # TODO А зачем вообще тогда celery?
        tasks.refresh_account.apply_async(args = [ str(currency), str(self.request.user) ]).wait()

        context = super(AccountView, self).get_context_data(**kwargs)
        context["label"] = label
        context["ticker"] = currency.ticker
        context["balance"] = account.get_obj().balance()

        return context

    def get_queryset(self):

        label = self.kwargs["label"]
        currency = get_object_or_404(Currency, label = label)
        account = get_object_or_404(Account, currency = currency, name = self.request.user)

        return Transaction.objects.filter(account = account).order_by("-pk")

class AddressView(LoginRequiredMixin, ListView):

    template_name = "address.html"

    def get_queryset(self):

        label = self.kwargs["label"]
        currency = get_object_or_404(Currency, label = label)
        account = get_object_or_404(Account, currency = currency, name = self.request.user)

        return Address.objects.filter(account = account).order_by("address")

#############################################################################

def create_address_modal(request, label):

    if request.method == "POST":

        account_name = str(request.user)

        result = tasks.create_address.apply_async(args = [ label, account_name ])
        result.wait()

        context = \
        {
            "address" : result.get()
        }

        return HttpResponse(json.dumps(context), content_type = "application/json")

    return HttpResponse(json.dumps({}), content_type = "application/json")

def exchange(request):

    template = loader.get_template("exchange.html")

    context = { "object_list" : [] }
    objs = Exchange.objects.raw("select coin_exchange.*, ca1.balance as balance_from, cc1.ticker as ticker_from, ca2.balance as balance_to, cc2.ticker as ticker_to from coin_exchange inner join coin_account as ca1 on coin_exchange.currency_from_id = ca1.currency_id inner join coin_account as ca2 on coin_exchange.currency_to_id = ca2.currency_id inner join coin_currency as cc1 on cc1.label = ca1.currency_id inner join coin_currency as cc2 on cc2.label = ca2.currency_id where ca1.name = ca2.name and ca1.name = 'admin' order by coin_exchange.currency_from_id;")

    for obj in objs:

        context["object_list"].append(
        {
            "id" : obj.id,
            "label" : obj.label,
            "balance_from" : obj.balance_from,
            "ticker_from" : obj.ticker_from,
            "balance_to" : obj.balance_to,
            "ticker_to" : obj.ticker_to,
            "currency_from" : obj.currency_from,
            "currency_to" : obj.currency_to,
            "coef" : obj.get_obj().coef(),
            "fee" : obj.fee
        })

    return HttpResponse(template.render(context, request))

def exchange_modal(request, _id):

    if request.method == "POST":

        try:

            account_name = str(request.user)
            amount = float(request.POST.get("amount"))
        
            # TODO А зачем вообще тогда celery?
            result = tasks.exchange.apply_async(args = [ _id, account_name, amount ])
            result.wait()
            error = result.get()

            if error is None:

                return HttpResponse(json.dumps({ "error" : None }), content_type = "application/json")

        except ValueError:

            error_code = 1

        return HttpResponse(json.dumps({ "error" : error_code }), content_type = "application/json")

    return HttpResponse(json.dumps({}), content_type = "application/json")

def send_modal(request, label):

    if request.method == "POST":

        error_code = 0

        try:

            account_name = str(request.user)
            address = request.POST.get("address")
            amount = float(request.POST.get("amount"))

            # TODO А зачем вообще тогда celery?
            result = tasks.send.apply_async(args = [ label, account_name, address, amount ])
            result.wait()
            error = result.get()

            if error is None:

                return HttpResponse(json.dumps({ "error" : None }), content_type = "application/json")

        except ValueError:

            error_code = 1

        return HttpResponse(json.dumps({ "error" : error_code }), content_type = "application/json")

#############################################################################

wallet = WalletView.as_view()
account = AccountView.as_view()
address = AddressView.as_view()

