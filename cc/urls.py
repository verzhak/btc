
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_view

urlpatterns = \
[
    url("^admin/", admin.site.urls),
    url("^accounts/", include("registration.backends.hmac.urls")),
    url(r"^coin/", include("coin.urls")),
    url(r"^pool/", include("pool.urls")),
    url(r"^device/", include("device.urls")),
    url(r"", include("home.urls")),
]

