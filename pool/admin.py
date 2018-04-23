
from django.contrib import admin

from . import models

class PoolAdmin(admin.ModelAdmin):
    
    list_display = ("currency", "label", "program", "host", "login", "password", "args", "priority", "is_enable", "is_login_need_suffix")

admin.site.register(models.Pool, PoolAdmin)

