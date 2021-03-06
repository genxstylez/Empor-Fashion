# coding: utf-8
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from empor.shortcuts import JsonResponse
from cart.utils import archive_cart
from cart.models import CartItem, ArchivedCartItem
from cart.views import get_cart
from discount.models import Voucher
from order.models import OrderItem, Order
from order.forms import OrderForm
from django.conf import settings

@login_required
def index(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        voucher_code = request.POST.get('voucher_code', None)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.discount_total = cart.discount_total
            order.gross_total = cart.gross_total
            order.net_total = cart.net_total
            order.user = request.user
            order.voucher_code = voucher_code
            order.order_id = ''
            order.billing_post_code = request.POST['billing_zip']
            order.billing_county = request.POST['billing_county']
            order.billing_district = request.POST['billing_district']
            order.shipping_post_code = request.POST['shipping_zip']
            order.shipping_county = request.POST['shipping_county']
            order.shipping_district = request.POST['shipping_district']
            order.save()
            request.session.save()
            request.session['order'] = order
            
            if order.payment_method == 0: 
                return redirect('order-paypal')
            else:
                return redirect('order-success')
    else:
        profile = request.user.profile
        form = OrderForm(initial={
                'billing_recipient': request.user.get_name(),
                'billing_phone' : profile.phone,
                'billing_address': profile.address,
                'billing_country': profile.country,
                'payment_method': 0,
                'reciept_type': 0,
                'dispatch_time': 0,
            }
        )
    try:
        voucher = request.session['voucher']
    except KeyError:
        voucher = None

    return render(request, 'order/index.html', {'cart': cart, 'form': form, 'items': items, 'voucher': voucher})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'order/orders.html', {'orders': orders})
    
@login_required
def info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    try:
        voucher = Voucher.objects.get(code=order.voucher_code)
    except Voucher.DoesNotExist:
        voucher = None

    if order.user != request.user:
        raise Http404

    return render(request, 'order/order.html', {'order': order, 'items': items, 'voucher': voucher})

@login_required
def paypal(request):
    try:
        order = request.session['order']
    except KeyError:
        raise Http404
    if order.user != request.user:
        raise Http404
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    
    return render(request, 'order/paypal.html', {'order': order, 'items': items, 'debug': settings.DEBUG})

@login_required
def success(request):
    from order.utils import generate_order_pdf
    from django.template.loader import render_to_string
    from django.core import mail
    from django.core.mail import EmailMultiAlternatives, EmailMessage
    from django.contrib.auth.models import Group
    try:
        order = request.session['order']
    except KeyError:
        raise Http404
    if order.user != request.user:
        raise Http404

    cart = get_cart(request)
    cart = archive_cart(cart)
    order.cart = cart.id
    order.save()
    del request.session['cart']
    voucher = request.session['voucher'] if 'voucher' in request.session else None

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

    pdf = generate_order_pdf(request.get_host(), order, voucher)

    subject = _('EMPOR Order Confirmation')
    html_content = render_to_string('order/email.html', {
        'order': order, 
        'items': items,
        'voucher': voucher,
        'STATIC_URL': settings.STATIC_URL, 
        'host': request.get_host()
    })
    text_content = render_to_string('order/email.txt', {
        'order': order,
        'voucher': voucher,
        'items': items,
        'host': request.get_host()
    })

    connection = mail.get_connection()
    connection.open()

    message = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [order.user.email])
    message.attach_alternative(html_content, 'text/html')
    filename = order.order_id
    message.attach(filename.encode('utf-8'), pdf, 'application/pdf')

    group = Group.objects.get(name='Service').user_set.only('email')
    subject = 'EMPOR - 新訂單 %s' % order.order_id
    group_email = [ user.email for user in group ]
    notification = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, group_email)
    notification.content_subtype = 'html'
    
    connection.send_messages([message, notification])
    connection.close()

    if 'voucher' in request.session:
        del request.session['voucher']
    return redirect('order-thankyou')

@login_required
def thankyou(request):
    if 'order' in request.session:
        order = request.session['order']
        if 'cart' in request.session:
            del request.session['cart']
    else:
        order = None
    return render(request, 'order/thankyou.html', {'order': order})

@login_required
def voucher_check(request):
    try:
        request.session['voucher']
        return JsonResponse({'success': False})
    except KeyError:
        cart = get_cart(request)
        code = request.POST.get('voucher_code', None)

        if code:
            voucher = Voucher.objects.get(code=code)
            value = voucher.get_value()
            if voucher.active:
                if voucher.percentage:
                    margin = int(cart.net_total * value)
                    cart.discount_total += margin
                    cart.net_total -= margin
                else:
                    cart.net_total -= value
                    cart.discount_total += value
            cart.save()
            request.session['cart'] = cart
            request.session['voucher'] = voucher
            return JsonResponse({
                'success': True, 
                'gross': cart.gross_total, 
                'discount': cart.discount_total, 
                'net': cart.net_total, 
                'voucher_name': voucher.name,
                'voucher_value': voucher.get_display_value(),
            })
        return JsonResponse({'success': False})

@login_required
def voucher_reset(request):
    try:
        cart = get_cart(request)
        voucher = request.session['voucher']
        value = voucher.get_value()
        if voucher.percentage:
            total = int(cart.net_total / float(1 - value))
            cart.discount_total -= int(total * float(value))
            cart.net_total = total
        else:
            cart.net_total += value
            cart.discount_total -= value

        cart.save()
        request.session['cart'] = cart
        del request.session['voucher']

        return JsonResponse({
            'success': True,
            'gross': cart.gross_total, 
            'discount': cart.discount_total,
            'net': cart.net_total,
        })
    except KeyError:
        return JsonResponse({'success': False })

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

