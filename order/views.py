# coding: utf-8
from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from empor.shortcuts import JsonResponse
from cart.utils import archive_cart
from cart.models import CartItem
from cart.views import get_cart
from order.models import OrderItem, Order
from order.forms import OrderForm
from django.conf import settings

@login_required
def index(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.discount_total = cart.discount_total
            order.gross_total = cart.gross_total
            order.net_total = cart.net_total
            order.cart = cart
            order.user = request.user
            order.shipping = get_shipping(request, order.country)
            order.save()
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
    
    return render(request, 'order/index.html', {'cart': cart, 'form': form, 'items': items})

@login_required
def get_shipping(request, country_id):
    country_id = int(country_id)
    if country_id > 0:
        if request.is_ajax():
            return JsonResponse({'success': True, 'shipping': settings.SHIPPING_OVERSEAS_COST})
        return settings.SHIPPING_OVERSEAS_COST
    else:
        cart = get_cart(request)
        if settings.SHIPPING_FREE_ITEM_COUNT:
            if cart.items.count() > settings.SHIPPING_FREE_ITEM_COUNT:
                if request.is_ajax():
                    return JsonResponse({'success': True, 'shipping': 0})
                return 0
        if settings.SHIPPING_FREE_MINIMUM_PURCHASE:
            if cart.net_total > settings.SHIPPING_FREE_MINIMUM_PURCHASE:
                if request.is_ajax():
                    return JsonResponse({'success': True, 'shipping': 0})
                return 0
        if request.is_ajax():
            return JsonResponse({'success': True, 'shipping': settings.SHIPPING_DEFAULT_COST})
        return settings.SHIPPING_DEFAULT_COST

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'order/orders.html', {'orders': orders})
    
@login_required
def info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)

    if order.user != request.user:
        raise Http404

    return render(request, 'order/order.html', {'order': order, 'items': items})

@login_required
def paypal(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    if order.user != request.user:
        raise Http404

    return render(request, 'order/paypal.html', {'order': order, 'items': items, 'debug': settings.DEBUG})

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

    cart = get_cart(request)
    archive_cart(cart)
    order.status = 1
    order.save()

    pdf = generate_order_pdf(request, order) 
    items = OrderItem.objects.filter(order=order)
    subject = _('EMPOR Order Confirmation')
    content = render_to_string('order/email.html', {'order': order, 'items': items, 
        'STATIC_URL': settings.STATIC_URL, 'domain': request.get_host()
    })
    message = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, [order.user.email])
    filename = order.order_id
    message.attach(filename.encode('utf-8'), pdf, 'application/pdf')
    message.content_subtype = "html"
    message.send()
    return render(request, 'order/thankyou.html', {'order': order})
