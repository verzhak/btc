
#
# Админка
#

from django.contrib import admin

from . import models

class CurrencyAdmin(admin.ModelAdmin):
    
    list_display = ("ticker", "label", "host")

class AccountAdmin(admin.ModelAdmin):

    list_display = ("currency", "name", "balance")

class AddressAdmin(admin.ModelAdmin):

    list_display = ("account", "address")

class TransactionAdmin(admin.ModelAdmin):

    list_display = ("account", "address", "category", "txid", "time", "amount", "fee", "confirmations")

class ExchangeAdmin(admin.ModelAdmin):

    # list_display = ("label", "currency_from", "currency_to", "coef", "fee") # TODO
    list_display = ("label", "currency_from", "currency_to", "fee")

admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.Exchange, ExchangeAdmin)

