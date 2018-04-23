
from django.db import models
from django.utils.translation import ugettext_lazy as _

from coin.models import Currency

class Pool(models.Model):

    currency = models.ForeignKey(Currency)
    label = models.CharField(_("Label"), max_length = 100, default = "", unique = True)
    program = models.CharField(_("Program"), default = "", max_length = 100)
    host = models.CharField(_("Host"), default = "", max_length = 100)
    login = models.CharField(_("Login"), default = "", max_length = 100)
    password = models.CharField(_("Password"), default = "", max_length = 100)
    args = models.TextField(_("Args"), default = "", blank = True, null = True)
    priority = models.PositiveIntegerField(_("Priority"), default = 0)
    is_enable = models.BooleanField(_("Is enable"), default = False)
    is_login_need_suffix = models.BooleanField(_("Is login need suffix"), default = False)

    __str__ = lambda self: self.label

    class Meta:

        verbose_name_plural = _("pools")

    def info(self, username):

        if self.is_login_need_suffix:

            login = "%s.%s" % (self.login, username)

        else:

            login = self.login

        content = \
        {
            "currency" :
            {
                "label" : self.currency.label
            },
            "label" : self.label,
            "program" : self.program,
            "host" : self.host,
            "login" : login,
            "password" : self.password,
            "args" : self.args,
            "priority" : self.priority
        }

        return content

