from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from member.settings import COUNTRY_CHOICES
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='profile', unique=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    billing_recipient = models.CharField(_('Billing recipient'), max_length=100)
    billing_street1 = models.CharField(_('Billing Street 1'), max_length=100)
    billing_street2 = models.CharField(_('Billing Street 2'), max_length=100, blank=True)
    billing_city = models.CharField(_('Billing City'), max_length=100)
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    shipping_recipient = models.CharField(_('Shipping recipient'), max_length=100)
    shipping_street1 = models.CharField(_('Shipping Street 1'), max_length=100)
    shipping_street2 = models.CharField(_('Shipping Street 2'), max_length=100, blank=True)
    shipping_city = models.CharField(_('Shipping City'), max_length=100)
    shipping_post_code = models.CharField(_('Shipping Post Code'), max_length=100)
    shipping_country = models.PositiveIntegerField(_('Shipping Country'), choices=COUNTRY_CHOICES, default=0)
