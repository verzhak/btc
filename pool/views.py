
import json, requests as req, time, hmac, hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.list import ListView

from lib import LoginRequiredMixin
from .models import Pool

def todo(login, ticker, ticker_full):

    key = "9ff787208f0140b0a4a1ffb890f6b6a7"
    secret = "e02ee0d6d6cc4e7783d65774bdc83f74"

    nonce = str(int(time.time() * 1000))
    username = "verzhak"
    message = username + key + nonce
    signature = hmac.new(secret.encode(), msg = message.encode(), digestmod = hashlib.sha256).hexdigest().upper()

    params = \
    {
        "key" : key,
        "nonce" : nonce,
        "signature" : signature,
        "coin" : ticker,
        "pageEnable" : 0,
        "pageSize" : 100 # TODO Должно работать и без pageSize, только с pageEnable
    }

    result = req.post("https://antpool.com/api/workers.htm", params = params)
    result = result.json()
    content = []

    if result["message"] == "ok":

        workers = result["data"]["rows"]

        for w in workers:

            name = w["worker"]
            sname = name.split(".")[1]

            if sname.find("777") >= 0:

                username, device = sname.split("777")

                if str(username).lower() == str(login).lower():

                    w["ticker"] = ticker_full
                    w["device"] = device

                    content.append(w)

    return content

class PoolView(LoginRequiredMixin, ListView):

    template_name = "pool.html"

    def get_context_data(self, **kwargs):

        context = super(PoolView, self).get_context_data(**kwargs)

        username = self.request.user
        context["stat"] = todo(username, "BTC", "Bitcoin") + todo(username, "LTC", "Litecoin") + todo(username, "DAS", "Dash")

        return context

    def get_queryset(self):

        return Pool.objects.filter(is_enable = True).order_by("-priority", "currency")

#############################################################################

pool = PoolView.as_view()

#############################################################################
# JSON-интерфейс

def get_miners(request, username = None):

    content = { "miners" : [] }

    if username is None:

        username = request.user.username

    for c in Pool.objects.filter(is_enable = True):

        content["miners"].append(c.info(username))

    return JsonResponse(content)

