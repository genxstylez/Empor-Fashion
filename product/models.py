# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from empor.storage import empor_storage
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext_lazy as _
from urllib import quote

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
    image = models.ImageField(_('Image'), upload_to=brand_path, storage=empor_storage)
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

class OptionGroup(models.Model):
    name = models.CharField(_('Option Group'), max_length=100)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(_('Option'), max_length=100)
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='options')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
    def __unicode__(self):
        return self.option_group.name + ' - ' + self.name

class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=True)
    sku = models.CharField(_('SKU'), max_length=20, blank=True)
    slug = models.CharField(_('Slug'), max_length=100, blank=True)
    description = models.TextField(_('Description'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    collection = models.ForeignKey(Collection, verbose_name=_('Collection'), related_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='products', null=True, blank=True)
    option = models.ForeignKey(Option, verbose_name=_('Option'), related_name='products', null=True, blank=True)
    price = models.PositiveIntegerField(_('Price'), default=0)
    composition = models.CharField(_('Composition'), max_length=100, blank=True)
    gender = models.ManyToManyField(Gender, related_name='products')
    discountable = models.BooleanField(_('Discountable'), default=False)
    featured = models.BooleanField(_('Featured'), default=False)
    has_options = models.BooleanField(_('Has options'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    class Meta:
        unique_together = ('slug', 'brand', 'option')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(' ', '').split('/')[0].lower() + '-' + self.id
        super(Product, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.option:
            return self.brand.name + ' - ' + self.collection.name + ' - ' + self.name + ' - ' + self.option.name
            
        return self.brand.name + ' - ' + self.collection.name + ' - ' + self.name
    
    def get_name(self):
        return self.__unicode__()

    def get_siblings(self):
        return self.collection.products.filter(parent=None).exclude(id=self.id)

    def get_main_image(self):
        return self.images.get(main=True).image

    def get_discount_value(self):
        dis = None
        value = 0 
        for discount in self.discount_set.all():
            if discount.percentage or discount.amount:
                if discount.percentage:
                    value2 = self.price * discount.percentage/100

                else:
                    value2 = int(discount.amount)

                if value2 > value:
                    value = value2
                    dis = discount
        return dis.percentage if dis.percentage else dis.amount

    def get_best_discount(self):
        dis = None
        value = 0 
        for discount in self.discount_set.all():
            if discount.percentage or discount.amount:
                if discount.percentage:
                    value2 = self.price * discount.percentage/100

                else:
                    value2 = int(discount.amount)

                if value2 > value:
                    value = value2
                    dis = discount
        return dis

    def get_discount_price(self):
        value = 0 
        if self.discountable:
            for discount in self.discount_set.all():
                if discount.percentage or discount.amount:
                    if discount.percentage:
                        value2 = self.price * discount.percentage/100

                    else:
                        value2 = int(discount.amount)

                    if value2 > value:
                        value = value2
        return value


    def get_discounted_price(self):
        value = 0 
        if self.discountable:
            for discount in self.discount_set.all():
                if discount.percentage or discount.amount:
                    if discount.percentage:
                        value2 = self.price * discount.percentage/100

                    else:
                        value2 = int(discount.amount)

                    if value2 > value:
                        value = value2
        return self.price - value

    @models.permalink
    def get_absolute_url(self):
        return ('product.views.product_view', [self.brand.name, self.slug])

@receiver(post_save, sender=Product)
def calculate_stock(sender, instance, **kwargs):
    total_stock = 0
    if instance.parent:
        for product in instance.parent.children.all():
            total_stock += product.stock
        instance.parent.stock = total_stock
        instance.parent.save()

@receiver(post_save, sender=Product)
def sku(sender, instance, **kwargs):
    if not instance.sku:
        if instance.parent: 
            instance.sku = instance.brand.name[:3].upper() + '%04d%04d%04d' % (instance.collection.id , instance.parent.id, instance.id)
        else:
            instance.sku = instance.brand.name[:3].upper() + '%04d%04d' % (instance.collection.id , instance.id)
        instance.save()

class ProductThumb(models.Model):

    def thumbnail_path(self, filename):
        return '%s/%s/%s/thumbnails/%s_thumbnail.%s' % (self.product.brand.name, self.product.collection.name, self.product.name.replace(' ', '').replace('/', '-'), filename.split('.')[0], filename.split('.')[1])
    def original_path(self, filename):
        return '%s/%s/%s/thumbnails/%s_original.%s' % (self.product.brand.name, self.product.collection.name, self.product.name.replace(' ', '').replace('/', '-'), filename.split('.')[0], filename.split('.')[1])

    product = models.OneToOneField(Product, verbose_name=_('Product'), related_name="thumb", null=True, blank=True)
    original = models.ImageField(upload_to=original_path, storage=empor_storage)
    thumb = models.ImageField(upload_to=thumbnail_path, blank=True, storage=empor_storage)
    x1 = models.IntegerField(default=0)
    y1 = models.IntegerField(default=0)
    x2 = models.IntegerField(default=0)
    y2 = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '<%s> %s' % (self.product.collection.name , self.product.name)

class ProductImage(models.Model):

    def product_image_path(self, filename):
        return '%s/%s/%s/images/%s' % (self.product.brand.name, self.product.collection.name, self.product.name.replace(' ', '').replace('/', '-'), filename)

    product = models.ForeignKey(Product, related_name='images')
    image = ThumbnailerImageField(_('Image'), upload_to=product_image_path, storage=empor_storage)
    main = models.BooleanField(_('Main'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)


