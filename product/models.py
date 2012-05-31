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
    has_options = models.BooleanField(_('Has options'), default=False)
    
    def __unicode__(self):
        return self.name

class OptionProduct(models.Model):
    description = models.TextField(_('Description'))
    product = models.ForeignKey(Product, verbose_name=_('Main product'), related_name='option_products')
    stock = models.IntegerField(_('Stock'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='option_products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='option_products')
    price = models.PositiveIntegerField(_('Price'), default=0)
     
    def __unicode__(self):

        if self.option_set.count() > 0:
            name = '' 
            for option in self.option_set.all():
                name += ' - ' + option.name
            return self.product.name + name

        return self.product.name

    def save(self):
        total_stock = 0
        for option_product in self.product.option_products.all():
            total_stock += option_product.stock
        self.product.stock = total_stock + self.stock
        self.product.has_options = True
        self.product.save()

        super(OptionProduct, self).save()

    def get_price(self):
        if self.price > 0:
            return self.price
        else:
            return self.product.price


class ProductImage(models.Model):

    def product_image_path(self, filename):
        return 'product_images/%s/%s' % (self.product.brand, self.product)

    product = models.ForeignKey(Product, related_name='images', null=True, blank=True)
    option_product = models.ForeignKey(OptionProduct, related_name='images', blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to=product_image_path, blank=True)

class OptionGroup(models.Model):
    name = models.CharField(_('Option Group'), max_length=100)
    products = models.ManyToManyField(OptionProduct)

    def __unicode__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(_('Option'), max_length=100)
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='options')
    products = models.ManyToManyField(OptionProduct)
    
    def __unicode__(self):
        return self.name
