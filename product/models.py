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
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class ProductGroup(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    price = models.PositiveIntegerField(_('Price'), default=0)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='product_groups')
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    price = models.PositiveIntegerField(_('Price'), default=0)
    product_group = models.ForeignKey(ProductGroup, related_name='products', null=True, blank=True)
    has_options = models.BooleanField(_('Has options'), default=False)
    
    def __unicode__(self):
        if self.has_options:
            name = '' 
            for option in self.option_set.all():
                name += ' - ' + option.name
            return self.name + name

        return self.name


    def save(self):
        if self.product_group:
            self.has_options = True
            if self.price == 0:
                self.price = self.product_group.price
            total_stock = 0
            for option_product in self.product_group.products.all():
                total_stock += option_product.stock
                self.product_group.stock = total_stock + self.stock
                self.product_group.save()

        super(Product, self).save()

class ProductImage(models.Model):

    def product_image_path(self, filename):
        return 'product_images/%s/%s' % (self.product.brand, self.product)

    product = models.ForeignKey(Product, related_name='images', null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to=product_image_path, blank=True)

class OptionGroup(models.Model):
    name = models.CharField(_('Option Group'), max_length=100)
    products = models.ManyToManyField(Product)

    def __unicode__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(_('Option'), max_length=100)
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='options')
    products = models.ManyToManyField(Product)
    
    def __unicode__(self):
        return self.name
