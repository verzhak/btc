
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class LoginRequiredMixin(object):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        
        token = (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

        return token

account_activation_token = AccountActivationTokenGenerator()

