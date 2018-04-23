
from django.contrib import admin

from . import models

class DeviceAdmin(admin.ModelAdmin):
    
    list_display = ("label", "desc", "part_ind", "parts", "earning", "price", "user", "is_confirm")

admin.site.register(models.Device, DeviceAdmin)

