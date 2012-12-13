# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from discount.models import Discount, Voucher
from product.models import Product
from order.settings import ORDER_STATUS_CHOICES, PAYMENT_METHOD_CHOICES, RECIEPT_TYPE_CHOICES, DISPATCH_TIME_CHOICES
from member.settings import COUNTRY_CHOICES
from datetime import datetime

class Order(models.Model):
    order_id = models.CharField(_('Order ID'), max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, related_name='orders')
    cart = models.PositiveIntegerField(_('Archived Cart'), default=0)
    items = models.ManyToManyField(Product, verbose_name='items', through='OrderItem')
    status = models.PositiveSmallIntegerField(_('Status'), max_length=1, choices=ORDER_STATUS_CHOICES, default=0)
    voucher_code = models.CharField(_('Voucher Code'), max_length=50, null=True, blank=True)
    payment_method = models.PositiveSmallIntegerField(_('Payment method'), choices=PAYMENT_METHOD_CHOICES, default=0)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Totoal'), default=0)
    net_total = models.PositiveIntegerField(_('Net Total'), default=0) 
    billing_recipient = models.CharField(_('Billing Recipient'), max_length=100)
    billing_phone = models.CharField(_('Billing Phone'), max_length=50)
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=100)
    billing_address = models.CharField(_('Billing Address'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    shipping_recipient = models.CharField(_('Shipping recipient'), max_length=100)
    shipping_phone = models.CharField(_('Shipping Phone'), max_length=50)
    shipping_post_code = models.CharField(_('Shipping Post Code'), max_length=100)
    shipping_address = models.CharField(_('Shipping Address'), max_length=100, blank=True)
    shipping_country = models.PositiveIntegerField(_('Shipping Country'), choices=COUNTRY_CHOICES, default=0)
    dispatch_time = models.PositiveSmallIntegerField(_('Dispatch time'), choices=DISPATCH_TIME_CHOICES, default=0)
    reciept_type = models.PositiveSmallIntegerField(_('Reciept Type'), default=0, choices=RECIEPT_TYPE_CHOICES)
    uni_no = models.PositiveIntegerField(_('Uni No.',), null=True, blank=True)
    company_title = models.CharField(_('Company Title'), max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    dispatched_date = models.DateTimeField(_('Dispatched Date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 2:
            d = []
            for product in self.items.all():
                product.stock += OrderItem.objects.get(product=product, order=self).quantity
                product.save()
                if product.discountable:
                    discount = Discount.objects.get(id=product.discount_id)
                    if discount in d:
                        pass
                    else:
                        discount.numUses -= 1
                        discount.save()
                        d.append(discount)

        if self.status == 1:
            d = []
            for product in self.items.all():
                if product.discountable:
                    discount = Discount.objects.get(id=product.discount_id)
                    if discount in d:
                        pass
                    else:
                        discount.numUses += 1
                        discount.save()
                        d.append(discount)

        super(Order, self).save(*args, **kwargs)

    def get_voucher(self):
        return Voucher.objects.get(code=self.voucher_code).name

    def get_billing_address(self):
        address = self.billing_post_code + ' '
        address += self.get_billing_country_display() + ' '
        address += self.billing_address
        return address

    def get_shipping_address(self):
        address = self.shipping_post_code + ' '
        address += self.get_shipping_country_display() + ' '
        address += self.shipping_address
        return address

@receiver(post_save, sender=Order)
def order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = 'EMP%6s%04d' % (datetime.now().strftime('%y%m%d'), instance.id)
        instance.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    discount_total = models.PositiveIntegerField(_('Discount Total'), default=0)
    gross_total = models.PositiveIntegerField(_('Gross Totoal'), default=0)
    net_total = models.PositiveIntegerField(_('Total'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
