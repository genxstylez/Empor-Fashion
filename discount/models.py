from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Collection, Product, Category, Brand
from transmeta import TransMeta

class Discount(models.Model):
    __metaclass__ = TransMeta

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

    class Meta:
        translate = ('amount', )

    def save(self, *args, **kwargs):
        if not self.valid_products:
            if self.valid_collections:
                for collection in self.valid_collections:
                    self.valid_products += collection.products.all()
                    self.valid_products.save()
            if self.valid_categories:
                for category in self.valid_categories:
                    self.valid_products += category.products.all()
                    self.valid_products.save()
            if self.valid_brands:
                for brand in self.valid_brands:
                    self.valid_products += brand.products.all()
                    self.valid_products.save()
        super(Discount, self).save(*args, **kwargs)
