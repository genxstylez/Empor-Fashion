from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def __unicode__(self):
        return self.name 

class ProductGroup(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'))
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    sold = models.PositiveIntegerField(_('Sold'), default=0)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='products')
    product_group = models.ForeignKey(ProductGroup, verbose_name=_('Product Group'), related_name='products', null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), related_name='products')
    price = models.PositiveIntegerField(_('Price'), default=0)
    has_options = models.BooleanField(_('Has options'), default=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    
    def __unicode__(self):
        if self.has_options:
            name = '' 
            for option in self.option_set.all():
                name += ' - ' + option.name
            return self.name + name

        return self.name

    def get_siblings(self):
        return self.product_group.products.exclude(product=self)

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
        return 'product_images/%s/%s' % (self.product.brand, self.product)

    product = models.ForeignKey(Product, related_name='images', null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to=product_image_path, blank=True)
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
