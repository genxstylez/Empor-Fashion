# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from order.models import Order
from datetime import datetime, timedelta
from django.conf import settings

def clean_orders():
    orders = Order.objects.filter(created_at__lte=datetime.now()-timedelta(days=2), status=0)
    orders.update(status=2)
    message = '%s Orders Expired' % (orders.count())
    group = Group.objects.get(name='Admin').user_set.only('email')
    group_mail = [ user.email for user in group ]
    if orders:
        send_mail('Daily Orders Clean Up', message, settings.DEFAULT_FROM_EMAIL, group_mail , fail_silently=False)
