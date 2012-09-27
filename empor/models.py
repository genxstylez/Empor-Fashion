# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from empor.storage import empor_storage

class KeyImpression(models.Model):
    def key_impression_path(self, filename):
        return 'key_impressions/%s' % (filename)
    image = models.ImageField(_('Image'), upload_to=key_impression_path, storage=empor_storage)
    active = models.BooleanField(_('Active'), default=True)
    url = models.URLField(_('Link'))

    def save(self, *args, **kwargs):
        super(KeyImpression, self).save()
        KeyImpression.objects.exclude(id=self.id).update(active=False)

class Impression(models.Model):
    def impression_path(self, filename):
        return 'impressions/%s' % (filename)
    image = models.ImageField(_('Image'), upload_to=impression_path, storage=empor_storage)
    active = models.BooleanField(_('Active'), default=True)
