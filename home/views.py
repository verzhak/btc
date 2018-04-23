
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login,  authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from lib import *

def home(request):

    if request.user.is_authenticated():

        return HttpResponseRedirect("/coin/")

    return render(request, "about.html")

def signin(request):
    
    error_code = 0
    
    if request.method == "POST":
        
        _login = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(username = _login, password = password)

        if user is not None:
            
            if user.is_active:
                
                login(request, user)
                
                return HttpResponse(json.dumps({ "error" : None }), content_type = "application/json")
            
            error_code = 1
            
        else:
                
            error_code = 2
                
    context = { "error": error_code }
        
    return HttpResponse(json.dumps({ "error" : error_code }), content_type = "application/json")

def signup(request):

    error_code = 1
    
    if request.method == "POST":
        
        _login = request.POST["login"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:

            if not (_login and email and password):

                error_code = 2

            else:

                user = User.objects.create_user(_login, email, password)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = _("Activate your account")
                message = render_to_string("activation_email.txt",
                {
                    "user" : user, 
                    "domain" : "btc.mir.sg", # TODO Костыль
                    "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                    "token" : account_activation_token.make_token(user),
                })
                EmailMessage(mail_subject, message, to = [ email ]).send()

                return HttpResponse(json.dumps({ "error" : None }), content_type = "application/json")
            
        except:
            
            pass
                
    return HttpResponse(json.dumps({ "error" : error_code }), content_type = "application/json")

def activate(request, uidb64, token):

    try:
        
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):

        user = None

    template = loader.get_template("activate.html")

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()

        message = _("Thank you for your email confirmation. Now you can login your account.")

    else:

        message = _("Activation link is invalid!")

    context = \
    {
        "message" : message
    }

    return HttpResponse(template.render(context, request))

