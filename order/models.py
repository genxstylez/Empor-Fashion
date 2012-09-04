# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from discount.models import Discount
from cart.models import ArchivedCart, ArchivedCartItem
from order.settings import ORDER_STATUS_CHOICES, PAYMENT_METHOD_CHOICES
from member.settings import COUNTRY_CHOICES
from datetime import datetime

class Order(models.Model):
    order_id = models.CharField(_('Order ID'), max_length=20, blank=True)
    user = models.ForeignKey(User, related_name='orders')
    cart = models.OneToOneField(ArchivedCart, related_name='order')
    items = models.ManyToManyField(Product, verbose_name='items', through='OrderItem')
    new = models.BooleanField(_('New'), default=True)
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES, default=0)
    payment_method = models.PositiveSmallIntegerField(_('Payment method'), max_length=1, choices=PAYMENT_METHOD_CHOICES)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Totoal'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0) 
    shipping_discount = models.PositiveIntegerField(_('Shipping Discount'), default=0)
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
    dispatched_date = models.DateTimeField(_('Dispatched date'), null=True, blank=True)

    def save(self):
        if self.status == 2:
            for product in self.items.all():
                product.stock += OrderItem.objects.get(product=product, order=self).quantity
                product.save()
                if product.discountable:
                    discount = ArchivedCartItem.objects.get(archived_cart=self.cart, product=product).discount
                    discount.numUses -= 1
                    discount.save()

        if self.status == 1:
            if self.items.count() > 1:
                self.shipping_discount = self.shipping.cost
            for product in self.items.all():
                if product.discountable:
                    discount = ArchivedCartItem.objects.get(archived_cart=self.cart, product=product).discount
                    discount.numUses += 1
                    discount.save()
        super(Order, self).save()

    def get_billing_address(self):
        address = self.billing_post_code + ' '
        address += self.get_billing_country_display()
        address += self.billing_city
        address += self.billing_street1
        if self.billing_street2:
            address += self.billing_street2
        return address

    def get_shipping_address(self):
        address = self.shipping_post_code
        address += self.get_shipping_country_display()
        address += self.shipping_city
        address += self.shipping_street1
        if self.shipping_street2:
            address += self.shipping_street2
        return address

@receiver(post_save, sender=Order)
def order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = 'EMP%6s%04d' % (datetime.now().strftime('%y%m%d'), instance.id)
        instance.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    discount = models.ForeignKey(Discount, verbose_name=_('Discount'), null=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Totoal'), default=0)
    net_total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    def save(self):
        self.product.stock = self.product.stock - self.quantity
        self.product.save()
        super(OrderItem, self).save()


