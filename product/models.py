from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
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
    
    def __unicode__(self):
        return self.name

class Product(models.Model):

    def thumbnail_path(self, filename):
        return 'product_images/%s/%s/thumbnail.%s' % (self.product.brand, self.product, self.filename.split('.')[1])

    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    collection = models.ForeignKey(Collection, verbose_name=_('Collection'), related_name='products')
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True)
    price = models.PositiveIntegerField(_('Price'), default=0)
    material = models.CharField(_('Material'), max_length=100, blank=True)
    featured = models.BooleanField(_('Featured'), default=False)
    has_options = models.BooleanField(_('Has options'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    
    def __unicode__(self):
        if self.has_options:
            name = '' 
            for option in self.option_set.all():
                name += ' - ' + option.name
            return self.product_group.name + ' - ' + self.name + name

        return self.product_group.name + ' - ' + self.name

    def get_siblings(self):
        return self.product_group.products.exclude(product=self)

    def get_main_product(self):
        return self.images.get(main=True)

    @models.permalink
    def get_absolute_url(self):
        return ('product.views.site.product_view', [self.name])

    def sold(self, qty):
        self.sold += qty
        self.stock -= qty
        if self.product_group:
            self.product_group.stock -= qty
            self.product_group.sold += qty
            self.product_group.save()
        if self.parent:
            self.parent.stock -= qty
            self.parent.stock += qty
            self.parent.save()
        super(Product, self).save()
    
    def deferr(self, qty):
        self.sold -= qty
        self.stock += qty
        if self.product_group:
            self.product_group.stock += qty
            self.product_group.sold -= qty
            self.product_group.save()
        if self.parent:
            self.parent.stock += qty
            self.parent.sold -= qty
            self.parent.save()
        super(Product, self).save()

    def save(self):
        if not self.pk:
            if self.parent:
                if self.price == 0:
                    self.price = self.parent.price
                total_stock = 0
                for product in self.parent.children.all():
                    total_stock += product.stock
                self.parent.stock = total_stock + self.stock
                self.parent.save()

            if self.product_group:
                total_stock = 0
                for product in self.product_group.products.all():
                    total_stock += product.stock
                self.product_group.stock = total_stock + self.stock
                self.product_group.save()
                
        super(Product, self).save()

class ProductImage(models.Model):

    def product_image_path(self, filename):
        return 'product_images/%s/%s' % (self.product.brand, self.product, filename)

    product = models.ForeignKey(Product, related_name='images', null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to=product_image_path, blank=True)
    main = models.BooleanField(_('Main'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

class OptionGroup(models.Model):
    name = models.CharField(_('Option Group'), max_length=100)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(_('Option'), max_length=100)
    option_group = models.ForeignKey(OptionGroup, verbose_name=_('Option Group'), related_name='options')
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
    def __unicode__(self):
        return self.name
