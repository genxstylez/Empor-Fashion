from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True)
    email = models.EmailField(_('email'))
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES, default='1')
    browser = models.PositiveIntegerField(_('browser'), choices=BROWSER_CHOICES, blank=True, null=True)
    os = models.PositiveIntegerField(_('os'), choices=OS_CHOICES, blank=True, null=True)
    content = models.TextField(_('content'))
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default='1')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions') 
    
