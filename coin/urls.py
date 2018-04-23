
from django.conf.urls import url

from . import views

urlpatterns = \
[
    url(r"^$", views.wallet, name = "wallet"),
    url(r"^exchange/$", views.exchange, name = "exchange"),
    url(r"^exchange/(?P<_id>.+)/$", views.exchange_modal, name = "exchange_modal"),
    url(r"^(?P<label>[^/]+)/$", views.account, name = "account"),
    url(r"^(?P<label>[^/]+)/address/$", views.address, name = "address"),
    url(r"^(?P<label>[^/]+)/send/$", views.send_modal, name = "send"),
    url(r"^(?P<label>[^/]+)/create_address/$", views.create_address_modal, name = "create_address"),
]

