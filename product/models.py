from django.db import models
from django.db.models.signals import post_save
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext_lazy as _

class Gender(models.Model): 
    name = models.CharField(_('Name'), max_length=30) 

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    gender = models.ManyToManyField(Gender, related_name='categories')
    
    def __unicode__(self):
        if self.parent:
            return '%s:%s' % (self.parent, self.name)
        return self.name

class Brand(models.Model):
    def brand_path(self, filename):
            return 'brand_images/%s/%s' % (self.name, filename)
    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image'), upload_to=brand_path)
    description = models.TextField(_('Description'))
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name 

class Collection(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    brand = models.ForeignKey(Brand, verbose_name='Brand')
    category = models.ForeignKey(Category, verbose_name='Category')
    gender = models.ManyToManyField(Gender)
    
    def __unicode__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    collection = models.ForeignKey(Collection, verbose_name=_('Collection'), related_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    price = models.PositiveIntegerField(_('Price'), default=0)
    composition = models.CharField(_('Composition'), max_length=100, blank=True)
    gender = models.ManyToManyField(Gender, related_name='products')
    featured = models.BooleanField(_('Featured'), default=False)
    has_options = models.BooleanField(_('Has options'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        if self.has_options:
            name = '' 
            for option in self.options.all():
                name += ' - ' + option.name
            return self.collection.name + ' - ' + self.name + name

        return self.collection.name + ' - ' + self.name

    def get_siblings(self):
        return self.collection.products.exclude(product=self)

    def get_main_product(self):
        return self.images.get(main=True)

    @models.permalink
    def get_absolute_url(self):
        return ('product.views.site.product_view', [self.name])

class ProductThumb(models.Model):

    def thumbnail_path(self, filename):
            return 'thumbnails/%s_thumbnail.%s' % (filename.split('.')[0], filename.split('.')[1])
    def original_path(self, filename):
            return 'thumbnails/%s_original.%s' % (filename.split('.')[0], filename.split('.')[1])

    product = models.OneToOneField(Product, verbose_name=_('Product'), related_name="thumb", null=True, blank=True)
    original = models.ImageField(upload_to=original_path)
    thumb = models.ImageField(upload_to=thumbnail_path, blank=True)
    x1 = models.IntegerField(default=0)
    y1 = models.IntegerField(default=0)
    x2 = models.IntegerField(default=0)
    y2 = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '<%s> %s' % (self.product.collection.name , self.product.name)

class ProductImage(models.Model):

    def product_image_path(self, filename):
        return 'product_images/%s' % (filename)

    product = models.ForeignKey(Product, related_name='images', null=True, blank=True)
    image = ThumbnailerImageField(_('Image'), upload_to=product_image_path, blank=True)
    main = models.BooleanField(_('Main'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

class OptionGroup(models.Model):
    name = models.CharField(_('Option Group'), max_length=100)
    products = models.ManyToManyField(Product, null=True, blank=True, related_name="option_group")
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(_('Option'), max_length=100)
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='options')
    products = models.ManyToManyField(Product, null=True, blank=True, related_name="options")
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
    def __unicode__(self):
        return self.option_group.name + ' - ' + self.name

def calculate_stock(sender, instance, **kwargs):
    total_stock = 0
    if instance.parent:
        for product in instance.parent.children.all():
            total_stock += product.stock
        instance.parent.stock = total_stock
        instance.parent.save()

post_save.connect(calculate_stock, sender=Product, dispatch_uid='calculate-stock')
