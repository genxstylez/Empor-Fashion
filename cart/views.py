from django.db import IntegrityError
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product
from cart.models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated():
        cart = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.get_or_create(session=request.session.session_key)
    return cart

def index(request):
    cart = get_cart(request)

    return render(request, 'cart/site/index.html', {'cart': cart})

def add_item(request, product_id, quantity):
    cart = get_cart(request)

    product = get_object_or_404(Product, id=product_id)

    try:
        item = CartItem.objects.get(product=product, cart=cart)
        item.quantity += quantity
        item.save()
    except CartItem.DoesNotExist:
        item = CartItem()
        item.cart = cart
        item.product = product
        item.quantity = quantity
        item.save()

    return JsonResponse({'success': True})

def remove_item(request, product_id):
    cart = get_cart(request)

    product = get_object_or_404(Product, id=product_id)

    item = get_object_or_404(product=product, cart=cart)

    try:
        item.delete()

    except IntegrityError:
        return JsonResponse({'success': False})
        
    return JsonResponse({'success': True})
