from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from cart.models import ArchivedCart
from order.settings import ORDER_STATUS_CHOICES, PAYMENT_METHOD_CHOICES

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    cart = models.OneToOneField(ArchivedCart, related_name='order')
    receiver = models.CharField(_('Receiver'), max_length=100)
    shipping_address = models.CharField(_('Address'), max_length=500)
    billing_address = models.CharField(_('Billing Address'), max_length=500)
    new = models.BooleanField(_('New'), default=True)
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES)
    payment_method = models.PositiveSmallIntegerField(_('Payment method'), max_length=1, choices=PAYMENT_METHOD_CHOICES)
    total = models.PositiveIntegerField(_('Total'), default=0) 
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        if self.status == 2:
            for product in self.products.all():
                product.product.stock+=product.quantity
                product.product.save()

        super(Order, self).save()
    
class OrderProducts(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'), related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        self.product.update(stock=self.product.stock - self.quantity)
        super(OrderProducts, self).save()

