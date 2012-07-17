from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.utils import archive_cart
from cart.views.site import get_cart
from order.models import OrderProduct
from order.forms import OrderForm

@login_required
def index(request):
    if request.user.is_anonymous():
        redirect('%s?next=%s' % (reverse('member-signin-register'), reverse('order-index')))

    else:
        cart = get_cart(request)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                a_cart = archive_cart(cart)
                order.total = a_cart.total
                order.cart = a_cart
                order.user = request.user
                order.save()
                for item in a_cart.items.all():
                    order_item = OrderProduct()
                    order_item.order = order
                    order_item.product = item.product
                    order_item.quantity = item.quantity
                    order_item.total = item.total
                    order_item.save()
        else:
            form = OrderForm(
                initial={
                    'billing_address': request.user.profile.get_billing_details(),
                    'shipping_address': request.user.profile.get_shipping_details()
                }
            )
        
        return render(request, 'order/site/index.html', {'cart': cart, 'form': form})
