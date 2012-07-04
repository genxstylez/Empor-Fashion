from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='cart', null=True, blank=True)
    session = models.CharField(_('Session'), max_length=100, blank=True)
    total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'), related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    
class ArchivedCart(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='archived_cart', null=True, blank=True)
    session = models.CharField(_('Session'), max_length=100, blank=True)
    items = models.ManyToManyField(Product, through='ArchivedCartItem')
    created_at = models.DateTimeField(_('Created at'))
    last_modified = models.DateTimeField(_('Last modified'))

class ArchivedCartItem(models.Model):
    cart = models.ForeignKey(ArchivedCart, verbose_name=_('Archived Cart'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    created_at = models.DateTimeField(_('Created at'))
    last_modified = models.DateTimeField(_('Last modified'))
