from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from product.models import Collection, Product, Category, Brand

class Discount(models.Model):

    description = models.CharField(_('Description'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    start_date = models.DateTimeField(_('Start Date'), auto_now_add=True)
    end_date = models.DateTimeField(_('End Date'), auto_now=True)
    allowUses = models.IntegerField(_('Number of allowed uses'), default=0)
    numUses = models.IntegerField(_('Number of times already used'), default=0)
    amount = models.PositiveIntegerField(_('Amount'), null=True, blank=True)
    percentage = models.DecimalField(_('Percentage'), decimal_places=2, max_digits=5, null=True, blank=True)
    valid_products = models.ManyToManyField(Product, verbose_name=_('Valid Products'), null=True, blank=True)
    valid_collections = models.ManyToManyField(Collection, verbose_name=_('Valid Collections'), null=True, blank=True)
    valid_categories = models.ManyToManyField(Category, verbose_name=_('Valid Categories'), null=True, blank=True)
    valid_brands = models.ManyToManyField(Brand, verbose_name=_('Valid Brands'), null=True, blank=True)

def product_discountable(sender, instance, **kwargs):
    """
    if instance.valid_collections.count() > 0:
        for collection in instance.valid_collections.all():
            instance.valid_products.add(*collection.products.all())
            collection.products.update(discountable=True)
    if instance.valid_categories.count() > 0:
        for category in instance.valid_categories.all():
            instance.valid_products.add(*category.products.all())
            category.products.update(discountable=True)
    """
    if instance.valid_brands.count() > 0:
        for brand in instance.valid_brands.all():
            for product in brand.products.all():
                instance.valid_products.add(product.id)
            brand.products.update(discountable=True)

post_save.connect(product_discountable, sender=Discount) 
