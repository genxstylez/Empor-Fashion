from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from cart.models import Cart

ORDER_STATUS_CHOICES = (
    (0, _('Pending for payment')),
    (1, _('Paid')),
    (2, _('Deferred'))
)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    cart = models.OneToOneField(Cart, related_name='order')
    products = models.ManyToManyField(Product, through='OrderProducts')
    price = models.PositiveIntegerField(_('Price'))
    receiver = models.CharField(_('Receiver'), max_length=100)
    shipping_address = models.CharField(_('Address'), max_length=500)
    billing_addresss = models.CharField(_('Billing Address'), max_length=500)
    new = models.BooleanField(_('New'), default=True)
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        if self.status == 2:
            for product in self.products.all():
                product.product.stock+=product.quantity
                product.product.save()

        super(Order, self).save()
    
class OrderProducts(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        self.product.update(stock=self.product.stock - self.quantity)
        super(OrderProducts, self).save()

