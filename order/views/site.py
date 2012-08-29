# coding: utf-8
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.utils import archive_cart
from cart.models import ArchivedCartItem, CartItem
from cart.views.site import get_cart
from order.models import OrderItem, Order
from order.forms import OrderForm

@login_required
def index(request):
    #redirect('%s?next=%s' % (reverse('member-signin-register'), reverse('order-index')))
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            a_cart = archive_cart(cart)
            order.discount_total = a_cart.discount_total
            order.gross_total = a_cart.gross_total
            order.net_total = a_cart.net_total
            order.cart = a_cart
            order.user = request.user
            order.save()
            items = ArchivedCartItem.objects.filter(archived_cart=a_cart)
            for item in items:
                order_item = OrderItem()
                order_item.order = order
                order_item.discount = item.discount
                order_item.product = item.product
                order_item.quantity = item.quantity
                order_item.discount_total = item.discount_total
                order_item.gross_total = item.gross_total
                order_item.net_total = item.net_total
                order_item.save()
                request.session.save()
                request.session['order_id']  = order.id
            if order.payment_method == 0: 
                return redirect('order-paypal')
            else:
                return redirect('order-success')
    else:
        profile = request.user.profile
        form = OrderForm(initial={
                'billing_recipient': profile.billing_recipient,
                'billing_phone' : profile.phone,
                'billing_street1': profile.billing_street1,
                'billing_street2': profile.billing_street2,
                'billing_city': profile.billing_city,
                'billing_post_code': profile.billing_post_code, 
                'billing_country': profile.billing_country,
                'shipping_recipient': profile.shipping_recipient,
                'shipping_phone': profile.phone,
                'shipping_street1': profile.shipping_street1,
                'shipping_street2': profile.shipping_street2,
                'shipping_city': profile.shipping_city,
                'shipping_post_code': profile.shipping_post_code,
                'shipping_country': profile.shipping_country,
                'payment_method': '0'
            }
        )
    
    return render(request, 'order/site/index.html', {'cart': cart, 'form': form, 'items': items})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'order/site/orders.html', {'orders': orders})
    

@login_required
def info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)

    if order.user != request.user:
        raise Http404

    return render(request, 'order/site/order.html', {'order': order, 'items': items})

@login_required
def paypal(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    if order.user != request.user:
        raise Http404

    return render(request, 'order/site/paypal.html', {'order': order, 'items': items})

@login_required
def success(request):
    order_id = request.session['order_id']
    from order.utils import generate_order_pdf
    from django.conf import settings
    from django.template.loader import render_to_string
    from django.core.mail import EmailMessage

    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        raise Http404

    order.status = 1
    order.save()

    pdf = generate_order_pdf(request, order) 
    items = OrderItem.objects.filter(order=order)
    subject = _('EMPOR Order Confirmation')
    content = render_to_string('order/site/email.html', {'order': order, 'items': items})
    message = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, [order.user.email])
    filename = order.order_id
    message.attach(filename.encode('utf-8'), pdf, 'application/pdf')
    message.content_subtype = "html"
    message.send()
    return render(request, 'order/site/thankyou.html', {'order': order})
