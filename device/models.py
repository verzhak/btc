
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Device(models.Model):

    label = models.CharField(_("Device name"), max_length = 100, default = "")
    desc = models.TextField(_("Description"), default = "")
    part_ind = models.PositiveIntegerField(_("Part index"), default = 1, validators = [ MinValueValidator(1) ])
    parts = models.PositiveIntegerField(_("Number of parts"), default = 1, validators = [ MinValueValidator(1) ])
    earning = models.FloatField(_("Earnings (month)"), default = 0.01, validators = [ MinValueValidator(0) ])
    price = models.FloatField(_("Prince (month)"), default = 0.001, validators = [ MinValueValidator(0) ])
    user = models.ForeignKey(User, null = True)
    is_confirm = models.BooleanField(default = False)

    __str__ = lambda self: self.label

    class Meta:

        verbose_name_plural = _("devices")
        unique_together = ("label", "part_ind")

