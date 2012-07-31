from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from cart.models import ArchivedCart
from order.settings import ORDER_STATUS_CHOICES, PAYMENT_METHOD_CHOICES
from member.settings import COUNTRY_CHOICES

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    cart = models.OneToOneField(ArchivedCart, related_name='order')
    new = models.BooleanField(_('New'), default=True)
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES, default=0)
    payment_method = models.PositiveSmallIntegerField(_('Payment method'), max_length=1, choices=PAYMENT_METHOD_CHOICES)
    total = models.PositiveIntegerField(_('Total'), default=0) 
    billing_recipient = models.CharField(_('Billing recipient'), max_length=100)
    billing_phone = models.CharField(_('Billing Phone'), max_length=50)
    billing_street1 = models.CharField(_('Billing Street 1'), max_length=100)
    billing_street2 = models.CharField(_('Billing Street 2'), max_length=100, blank=True)
    billing_city = models.CharField(_('Billing City'), max_length=100)
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    shipping_recipient = models.CharField(_('Shipping recipient'), max_length=100)
    shipping_phone = models.CharField(_('Shipping Phone'), max_length=50)
    shipping_street1 = models.CharField(_('Shipping Street 1'), max_length=100)
    shipping_street2 = models.CharField(_('Shipping Street 2'), max_length=100, blank=True)
    shipping_city = models.CharField(_('Shipping City'), max_length=100)
    shipping_post_code = models.CharField(_('Shipping Post Code'), max_length=100)
    shipping_country = models.PositiveIntegerField(_('Shipping Country'), choices=COUNTRY_CHOICES, default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        if self.status == 2:
            for product in self.items.all():
                product.product.stock+=product.quantity
                product.product.save()

        super(Order, self).save()
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'), related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        self.product.stock= self.product.stock - self.quantity
        self.product.save()
        super(OrderProduct, self).save()

