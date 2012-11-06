from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from member.settings import COUNTRY_CHOICES, GENDER_CHOICES

class UserExtend(object):
    def is_authenticated(self):
        if self.profile.activated:
            return True
        return False

    def get_name(self):
        return self.first_name + ' ' + self.last_name

User.__bases__ += (UserExtend,)

class UserTemp(models.Model):
    username = models.CharField(_('username'), max_length=20)
    password = models.CharField(_('password'), max_length=128)
    email = models.EmailField(_('email'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.PositiveSmallIntegerField(_('Gender'), choices=GENDER_CHOICES, default=0)
    birthday = models.DateField(_('Birthday'))
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    billing_recipient = models.CharField(_('Billing recipient'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    billing_city = models.CharField(_('Billing City'), max_length=100)
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=100)
    billing_street1 = models.CharField(_('Billing Street 1'), max_length=100)
    billing_street2 = models.CharField(_('Billing Street 2'), max_length=100, blank=True)
    activation_code = models.CharField(max_length=40, db_index=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='profile', unique=True)
    gender = models.PositiveSmallIntegerField(_('Gender'), choices=GENDER_CHOICES, default=0)
    birthday = models.DateField(_('Birthday'))
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    billing_recipient = models.CharField(_('Billing recipient'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    billing_city = models.CharField(_('Billing City'), max_length=100)
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=100)
    billing_street1 = models.CharField(_('Billing Street 1'), max_length=100)
    billing_street2 = models.CharField(_('Billing Street 2'), max_length=100, blank=True)
    reset_code = models.CharField(max_length=40, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s's Profile" % self.user

class FacebookProfile(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='facebook_profile')
    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=15)
    locale = models.CharField(max_length=15)
    url = models.URLField(blank=True, null=True)
    timezone = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)
    access_token = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField()
