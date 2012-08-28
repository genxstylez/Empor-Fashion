from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from product.models import Product
from discount.models import Discount

class Cart(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='cart', null=True, blank=True)
    session = models.CharField(_('Session'), max_length=100, blank=True)
    items = models.ManyToManyField(Product, verbose_name=_('Items'), through='CartItem')
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Total'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'))
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='cart_items')
    discount = models.ForeignKey(Discount, verbose_name=_('Discount'), related_name='cart_items', null=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Total'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
class ArchivedCart(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='archived_cart', null=True, blank=True)
    session = models.CharField(_('Session'), max_length=100, blank=True)
    items = models.ManyToManyField(Product, verbose_name=_('Items'), through='ArchivedCartItem')
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Total'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0)
    created_at = models.DateTimeField(_('Created at'))
    last_modified = models.DateTimeField(_('Last modified'))

class ArchivedCartItem(models.Model):
    archived_cart = models.ForeignKey(ArchivedCart, verbose_name=_('Archived Cart'))
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='archived_cart_items')
    discount = models.ForeignKey(Discount, verbose_name=_('Discount'), related_name='archived_cart_items', null=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Total'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0)
    created_at = models.DateTimeField(_('Created at'))
    last_modified = models.DateTimeField(_('Last modified'))
