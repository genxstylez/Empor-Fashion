from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))

    def __unicode__(self):
        return self.name 

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    stock = models.IntegerField(_('Stock'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    price = models.PositiveIntegerField(_('Price'), default=0)
     
    def __unicode__(self):
        return self.name

class ProductImage(models.Model):

    def product_image_path(self, filename):
        return 'product_images/%s/%s' % (self.product.brand, self.product)

    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(_('Image'), upload_to=product_image_path, blank=True)

class ProductVariation(models.Model):
    name = models.CharField(_('Variation'), max_length=100)
    stock = models.IntegerField(_('Stock'), default=0)
    price = models.PositiveIntegerField(_('Price'), default=0)
    product = models.ForeignKey(Product, related_name='variations')

    def __unicode__(self):
        return self.name

    def save(self):
        total_stock = 0
        for variation in self.product.variations.all():
            total_stock += variation.stock
        self.product.stock = total_stock
        self.product.save()

        super(ProductVariation, self).save()

    def get_price(self):
        if self.price > 0:
            return self.price
        else:
            return self.product.price

class ProductVariationType(models.Model):
    name = models.CharField(_('Variation'), max_length=100)
    product = models.ManyToManyField(Product, blank=True)
    variations = models.ManyToManyField(ProductVariation, verbose_name=_('Variations'), blank=True)
    
    def __unicode__(self):
        return self.name


