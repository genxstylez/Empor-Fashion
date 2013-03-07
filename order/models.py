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
    billing_post_code = models.CharField(_('Billing Post Code'), max_length=5)
    billing_county = models.CharField(_('Billing County'), max_length=10)
    billing_district = models.CharField(_('Billing District'), max_length=10)
    billing_address = models.CharField(_('Billing Address'), max_length=100)
    billing_country = models.PositiveIntegerField(_('Billing Country'), choices=COUNTRY_CHOICES, default=0)
    shipping_recipient = models.CharField(_('Shipping recipient'), max_length=100)
    shipping_phone = models.CharField(_('Shipping Phone'), max_length=50)
    shipping_post_code = models.CharField(_('Shipping Post Code'), max_length=5)
    shipping_county = models.CharField(_('Shipping County'), max_length=10)
    shipping_district = models.CharField(_('Shipping District'), max_length=10)
    shipping_address = models.CharField(_('Shipping Address'), max_length=100)
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
                product.sold -= OrderItem.objects.get(product=product, order=self).quantity
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
                product.sold += OrderItem.objects.get(product=product, order=self).quantity
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
        address = self.get_billing_country_display() + ' '
        address += self.billing_post_code + ' '
        address += self.billing_county + ' '
        address += self.billing_district + ' '
        address += self.billing_address
        return address

    def get_shipping_address(self):
        address = self.get_shipping_country_display() + ' '
        address += self.shipping_post_code + ' '
        address += self.shipping_county + ' '
        address += self.shipping_district + ' '
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

from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged
from order.utils import generate_order_pdf
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from discount.models import Voucher
from cart.utils import archive_cart
from cart.models import ArchivedCartItem

def confirm_payment(sender, **kwargs):
    user = User.objects.get(id=sender.custom)
    cart = archive_cart(user.cart)
    order = Order.objects.get(id=sender.invoice)
    order.cart = cart.id
    order.save()
    
    items = ArchivedCartItem.objects.filter(archived_cart=cart)
    for item in items:
        order_item = OrderItem()
        order_item.order = order
        order_item.product = item.product
        order_item.quantity = item.quantity
        order_item.discount_total = item.discount_total
        order_item.gross_total = item.gross_total
        order_item.net_total = item.net_total
        order_item.save()
        #Update sold figure
        item.product.sold += item.quantity
        item.product.save()

    order.status = 1
    order.save()
    try: 
        voucher = Voucher.objects.get(code=order.voucher_code)
    except Voucher.DoesNotExist:
        voucher = None

    pdf = generate_order_pdf('empor.com.tw', order, voucher)

    subject = _('EMPOR Order Confirmation')
    html_content = render_to_string('order/email.html', {
        'order': order,
        'items': items,
        'voucher': voucher,
        'STATIC_URL': settings.STATIC_URL,
        'host': 'http://empor.com.tw/'
    })
    text_content = render_to_string('order/email.txt', {
        'order': order,
        'voucher': voucher,
        'items': items,
        'host': 'http://empor.com.tw/'
    })

    connection = mail.get_connection()
    connection.open()

    message = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [order.user.email])
    message.attach_alternative(html_content, 'text/html')
    filename = order.order_id
    message.attach(filename.encode('utf-8'), pdf, 'application/pdf')

    group = Group.objects.get(name='Service').user_set.only('email')
    subject = 'EMPOR - 新訂單'.decode('utf-8') + ' '+ order.order_id
    group_email = [ user.email for user in group ]
    notification = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, group_email)
    notification.content_subtype = 'html'

    connection.send_messages([message, notification])
    connection.close()
 
payment_was_successful.connect(confirm_payment)


def flag(sender, **kwargs):
    pass

payment_was_flagged.connect(flag)
