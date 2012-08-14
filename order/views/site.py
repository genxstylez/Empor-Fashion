from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.utils import archive_cart
from cart.models import ArchivedCartItem, CartItem
from cart.views.site import get_cart
from order.models import OrderProduct
from order.forms import OrderForm
from paypal.standard.forms import PayPalPaymentsForm

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
            order.total = a_cart.total
            order.cart = a_cart
            order.user = request.user
            order.save()
            items = ArchivedCartItem.objects.filter(archived_cart=a_cart)
            for item in items:
                order_item = OrderProduct()
                order_item.order = order
                order_item.product = item.product
                order_item.quantity = item.quantity
                order_item.total = item.total
                order_item.save()
                if item.discount:
                    item.discount.numUses += 1
                    item.discount.save()
            return render(request, 'order/site/thankyou.html', {'order': order})
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
    
    return render(request, 'order/site/index.html', {'cart': cart, 'form': form, 'items': items, 'paypal_form': paypal_form})
