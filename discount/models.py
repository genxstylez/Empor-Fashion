from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from product.models import Collection, Product, Category, Brand

class Discount(models.Model):
    name = models.CharField(_('Name'), max_length=100)
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
    
    def __unicode__(self):
        return self.name

    def save(self):
        if self.allowUses > 0 and self.numUses == self.allowUses:
            self.active = False

        if not self.active:
            for product in self.valid_products.all():
                discountable = False
                for discount in product.discount_set.exclude(id=self.id):
                    if discount.active:
                        discountable = True
                product.discountable = discountable
                product.save()

        super(Discount, self).save()

def products(sender, instance, action, **kwargs):
    if action == 'post_add':
        for product in instance.valid_products.all():
            if instance.active:
                product.discountable = True
                product.save()

def brand_products(sender, instance, action, **kwargs):
    if action == 'post_add':
        for brand in instance.valid_brands.all():
            instance.valid_products.add(*brand.products.all())
            if instance.active:
                brand.products.update(discountable=True) 

def collection_products(sender, instance, action, **kwargs):  
    if action == 'post_add':
        for collection in instance.valid_collections.all():
            instance.valid_products.add(*collection.products.all())
            if instance.active:
                collection.products.update(discountable=True)

def category_products(sender, instance, action, **kwargs):
    if action == 'post_add':
         for category in instance.valid_categories.all():
            instance.valid_products.add(*category.products.all())
            if instance.active:
                category.products.update(discountable=True)

m2m_changed.connect(products, sender=Discount.valid_products.through)
m2m_changed.connect(brand_products, sender=Discount.valid_brands.through)
m2m_changed.connect(collection_products, sender=Discount.valid_collections.through)
m2m_changed.connect(category_products, sender=Discount.valid_categories.through)
