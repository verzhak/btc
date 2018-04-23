
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.db.models import Q
from django.template import loader

from lib import LoginRequiredMixin
from .models import Device

class DeviceListView(LoginRequiredMixin, ListView):

    template_name = "device_list.html"

    def get_queryset(self):

        return Device.objects.filter(Q(user = self.request.user) | Q(user = None)).order_by("user", "-is_confirm", "label", "part_ind")

#############################################################################

def device(request):

    template = loader.get_template("device.html")

    return HttpResponse(template.render({}, request))

def device_toggle(request, _id):

    user = request.user
    device = Device.objects.get(pk = _id)
    device.is_confirm = False

    if device.user == user: device.user = None
    elif device.user == None: device.user = user
    
    device.save()

    return HttpResponse("")

#############################################################################

device_list = DeviceListView.as_view()

