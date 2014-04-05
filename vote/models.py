from django.db import models
from django.utils.translation import ugettext_lazy as _
from empor.storage import empor_storage

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    def vote_path(self, filename):
        return 'vote/%s/%s.%s' % (self.category.id, self.name, filename.split('.')[1])

    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='items')
    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image'), upload_to=vote_path, storage=empor_storage)
    vote_count = models.IntegerField(_('Vote Count'), default=0)

    def __unicode__(self):
        return self.name


