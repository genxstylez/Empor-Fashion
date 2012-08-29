from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from service.settings import TYPE_CHOICES, STATUS_CHOICES

class Question(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True)
    email = models.EmailField(_('Email'))
    type = models.PositiveSmallIntegerField(_('Type'), choices=TYPE_CHOICES, default=1)
    content = models.TextField(_('Content'))
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions') 
    
class Reply(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True)
    content = models.TextField(_('Content'))
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

