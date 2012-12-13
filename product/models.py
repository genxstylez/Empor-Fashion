# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from empor.storage import empor_storage
from discount.models import Discount
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext_lazy as _
import re

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

    def get_size(self, brand):
        try:
            size = SizeConversion.objects.get(category=self, brand=brand)
            return size
        except SizeConversion.DoesNotExist:
            if self.parent:
                self.parent.get_size(brand)
            else:
                return None

class Brand(models.Model):
    def brand_path(self, filename):
        return 'brand_images/%s/image.%s' % (self.name, filename.split('.')[1])
    
    def brand_w_path(self, filename):
        return 'brand_images/%s/image_w.%s' % (self.name, filename.split('.')[1])

    def story_path(self, filename):
        return 'brand_images/%s/story.%s' % (self.name, filename.split('.')[1])

    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image (Original)'), upload_to=brand_path, storage=empor_storage)
    w_image = models.ImageField(_('Image (White)'), upload_to=brand_w_path, storage=empor_storage, blank=True)
    story = models.ImageField(_('Story'), upload_to=story_path, storage=empor_storage, blank=True)
    slug = models.SlugField(_('Slug'), db_index=True)
    description = models.TextField(_('Description'))
    categories = models.ManyToManyField(Category, related_name='brands')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name 

    def get_men_categories(self):
        return self.categories.filter(gender__id=1)

    def get_women_categories(self):
        return self.categories.filter(gender__id=2)

    @models.permalink
    def get_absolute_url(self):
        return ('brand-view', [self.slug])

class SizeConversion(models.Model): 
    def size_path(self, filename):
        import uuid
        return 'brand_images/size/%s.%s' % (str(uuid.uuid4()), filename.split('.')[1])
    image = models.ImageField(_('Image'), upload_to=size_path, storage=empor_storage)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey(Category)

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

    def product_count(self):
        count = 0
        for product in self.products.filter(parent=None):
            count += product.stock
        return count

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

class ProductManager(models.Manager):
    def get_query_set(self):
        queryset = super(ProductManager, self).get_query_set()
        queryset = queryset.filter(parent=None)
        return queryset

class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    sku = models.CharField(_('SKU'), max_length=20, db_index=True)
    slug = models.SlugField(_('Slug'), db_index=True)
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
    remark = models.CharField(_('Remark'), max_length=100, null=True, blank=True)
    gender = models.ManyToManyField(Gender, related_name='products')
    discount_id = models.PositiveIntegerField(_('Discount'), default=0)
    discountable = models.BooleanField(_('Discountable'), default=False)
    featured = models.BooleanField(_('Featured'), default=False)
    has_options = models.BooleanField(_('Has options'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    objects = models.Manager()
    on_site = ProductManager()

    class Meta:
        unique_together = ('slug', 'brand', 'option')
    
    def __unicode__(self):
        if self.option:
            return self.name + ' - ' + self.option.name
            
        return self.name

    def discount(self):
        if self.discount_id > 0:
            return Discount.objects.get(id=self.discount_id)
        return None

    def save(self, *args, **kwargs):
        if not self.parent and self.id:
            for product in self.children.all():   
                if product.category != self.category or product.collection != self.collection or product.brand != self.brand:
                    product.category = self.category
                    product.collection = self.collection
                    product.brand = self.brand
                    product.save()

        if self.discount_id == 0:
            self.discountable = False
        else:
            self.discountable = True

        super(Product, self).save(*args, **kwargs)

    def get_name(self):
        return self.__unicode__()

    def get_size_conversion(self):
        size = self.category.get_size(self.brand)
        if size:
            return size.image.url
        return None

    def get_siblings(self):
        return self.collection.products.filter(parent=None).exclude(id=self.id)

    def get_main_image(self):
        return self.images.get(main=True)

    def get_gender(self):
        if self.gender.count() == 2:
            return 3
        else:
            return self.gender.all()[0].id

    def get_discount_value(self):
        discount = self.discount()
        return discount.get_value()

    def get_discount_price(self):
        discount = self.discount()
        value = discount.get_value()
        if discount.percentage:
            value = self.price * value
        return value

    def get_discounted_price(self):
        discount = self.discount()
        value = discount.get_value()
        if discount.percentage:
            value = self.price * value
        return self.price - value

    @models.permalink
    def get_absolute_url(self):
        return ('product-view', [self.brand.slug, self.gender.all()[0], self.slug])

@receiver(post_save, sender=Product)
def hierachy(sender, instance, **kwargs):
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
            value = Product.objects.filter(parent=instance.parent).count()
            instance.sku = instance.parent.sku + '%04d' % value
        else:
            value = Product.objects.filter(parent=None, brand=instance.brand, collection=instance.collection).count()
            instance.sku = re.sub(r'[\W_]', '', instance.brand.name)[:3].upper() + '%04d%04d' % (instance.collection.id , value)
        instance.save()

class ProductThumb(models.Model):
    def thumbnail_path(self, filename):
        return '%s/%s/%s/thumbnails/%s_thumbnail.%s' % (self.product.brand.name, self.product.collection.name, \
            self.product.name.replace(' ', '').replace('/', '-'), filename.split('.')[0], filename.split('.')[1])
    def original_path(self, filename):
        return '%s/%s/%s/thumbnails/%s_original.%s' % (self.product.brand.name, self.product.collection.name, \
            self.product.name.replace(' ', '').replace('/', '-'), filename.split('.')[0], filename.split('.')[1])

    product = models.OneToOneField(Product, verbose_name=_('Product'), related_name="thumb", null=True, blank=True)
    original = models.ImageField(upload_to=original_path, storage=empor_storage, max_length=255)
    thumb = models.ImageField(upload_to=thumbnail_path, blank=True, storage=empor_storage, max_length=255)
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
    image = ThumbnailerImageField(_('Image'), upload_to=product_image_path, storage=empor_storage, max_length=255)
    small_width = models.PositiveSmallIntegerField(default=0)
    small_height = models.PositiveSmallIntegerField(default=0)
    medium_width = models.PositiveSmallIntegerField(default=0)
    medium_height = models.PositiveSmallIntegerField(default=0)
    large_width = models.PositiveSmallIntegerField(default=0)
    large_height = models.PositiveSmallIntegerField(default=0)
    main = models.BooleanField(_('Main'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def delete(self):
        try:
            if empor_storage.exists(self.image.file.name):
                empor_storage.delete(self.image.file.name)
                empor_storage.delete(self.image['small'].file.name)
                empor_storage.delete(self.image['medium'].file.name)
                empor_storage.delete(self.image['large'].file.name)
        except IOError:
                pass
        super(ProductImage,self).delete()
