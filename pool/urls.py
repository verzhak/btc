
from django.conf.urls import url

from . import views

urlpatterns = \
[
    url(r"^$", views.pool, name = "pool"),
    url(r"^get_miners/(?P<username>.+)/$", views.get_miners, name = "get miners"),
    url(r"^get_miners/$", views.get_miners, name = "get miners"),
]

