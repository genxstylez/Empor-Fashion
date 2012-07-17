from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Collection, Product, Category, Brand

class Discount(models.Model):
    description = models.CharField(_('Description'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    start_date = models.DateTimeField(_('Start Date'), auto_now_add=True)
    end_date = models.DateTimeField(_('End Date'), auto_now=True)
    allowUses = models.IntergerField(_('Number of allowed uses'), default=0)
    numUses = models.IntegerField(_('Number of times already used'), default=0)
    amount = models.PositiveIntegerField(_('Amount'), null=True, Blank=True)
    percentage = models.DecimalField(_('Percentage'), null=True, Blank=True)
    valid_products = models.ManyToManyField(Product, verbose_name=_('Valid Products'), null=True, blank=True)
    valid_collections = models.ManyToManyField(Collection, verbose_name=_('Valid Collections'), null=True, blank=True)
    valid_categories = models.ManyToManyField(Category, verbose_name=_('Valid Categories'), null=True, blank=True)
    valid_brands = models.ManyToManyField(Brand, verbose_name=_('Valid Brands'), null=True, blank=True)

    class Meta:
        translate = ('amount')
