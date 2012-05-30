from django.db import models
from django.contrib.auth import User
from django.utils.translation import ugettext_lazy as _
from product.models import ProductVariation

ORDER_STATUS_CHOICES = (
    (0, _('Pending for payment')),
    (1, _('Paid')),
    (2, _('Deferred'))
)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    price = models.PositiveIntegerField(_('Price'))
    items = models.ManyToManyField(ProductVariation)
    shipping_address = models.CharField(_('Addresss'))
    billing_addresss = models.CharField(_('Billing Adress'))
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

