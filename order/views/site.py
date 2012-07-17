from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem, ArchivedCart, ArchivedCartItem
from cart.views.site import get_cart
from order.forms import OrderForm

@login_required
def index(request):
    if request.user.is_anonymous():
        redirect('%s?next=%s' % (reverse('member-signin-register'), reverse('order-index')))

    else:
        cart = get_cart(request)
        form = OrderForm(request.POST or None, 
            initial={
                'billing_address': request.user.profile.get_billing_details(),
                'shipping_address': request.user.profile.get_shipping_details()
            }
        )

        return render(request, 'order/site/index.html', {'cart': cart, 'form': form})
