# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from cart.models import Cart
from cart.utils import archive_cart
from datetime import datetime, timedelta
from django.conf import settings

def clean_carts():
    carts = Cart.objects.filter(created_at__lte=datetime.now()-timedelta(hours=12))
    for cart in carts:
        archive_cart(cart, 'revert')
    message = '%s Carts Expired' % (carts.count())
    group = Group.objects.get(name='Admin').user_set.only('email')
    group_mail = [ user.email for user in group ]
    send_mail('Daily Orders Clean Up', message, settings.DEFAULT_FROM_EMAIL, group_mail , fail_silently=False)
