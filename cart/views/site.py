from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product
from cart.models import Cart, CartItem
from cart.utils import archive_cart

def get_cart(request):
    try:
        cart_id = request.session['cart_id']
    except KeyError:
        cart_id = 0

    try:
        cart = Cart.objects.get(id=cart_id)
        if request.user.is_authenticated():
            if not cart == request.user.cart:
                archive_cart(request.user.cart)
                cart.user = request.user
                cart.save()

    except Cart.DoesNotExist:
        request.session.save()
        if request.user.is_authenticated():
            cart, created  = Cart.objects.get_or_create(user=request.user)
        else:
            cart, created = Cart.objects.get_or_create(session=request.session.session_key)

        request.session['cart_id']  = cart.id

    return cart

def index(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/site/index.html', {'cart': cart, 'items': items})

def add_item(request):
    cart = get_cart(request)
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        product = get_object_or_404(Product, id=product_id)

        #if no options selected for has_options product
        if product.has_options and product.children.count() > 0:
            return JsonResponse({'success': False})

        try:
            item = CartItem.objects.get(product=product, cart=cart)
        except CartItem.DoesNotExist:
            item = CartItem()
            item.cart = cart
            item.product = product

        quantity = int(quantity)
        item.quantity += int(quantity)
        item.discount_total += product.get_discount_price() * quantity
        item.total += product.get_discounted_price() * quantity
        item.save()
        cart.total += product.get_discounted_price() * quantity
        cart.discount_total += item.discount_total
        cart.save()

        items = CartItem.objects.filter(cart=cart)

        return render(request, 'cart/site/index-ajax.html', {'cart': cart, 'items': items})
    else: 
        return Http404

def remove_item(request, item_id):
    cart = get_cart(request)

    item = get_object_or_404(CartItem, id=item_id)

    try:
        total = item.total
        discount_total = item.discount_total
        item.delete()
        cart.discount_total -= discount_total
        cart.total -= total
        cart.save()
         
    except IntegrityError:
        return JsonResponse({'success': False})
        
    return JsonResponse({'success': True})
