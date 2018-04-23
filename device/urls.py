
from django.conf.urls import url

from . import views

urlpatterns = \
[
    url(r"^$", views.device, name = "device"),
    url(r"^device_list/$", views.device_list, name = "device_list"),
    url(r"^device_toggle/(?P<_id>.+)/$", views.device_toggle, name = "device_toggle"),
]

