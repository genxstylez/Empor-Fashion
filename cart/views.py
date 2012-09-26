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
            if cart != request.user.cart:
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
    return render(request, 'cart/index.html', {'cart': cart, 'items': items})

def add_item(request):
    cart = get_cart(request)
    if request.method == 'POST' and request.is_ajax():

        product_id = request.POST.get('product_id', None)
        quantity = request.POST.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        try:
            item = CartItem.objects.get(product=product, cart=cart)
        except CartItem.DoesNotExist:
            item = CartItem()
            item.cart = cart
            item.product = product
            item.discount = product.get_best_discount()

        quantity = int(quantity)
        discount = product.get_discount_price() * quantity
        gross = product.price * quantity
        item.quantity += int(quantity)
        item.discount_total += discount
        item.gross_total += gross
        item.net_total += gross - discount
        item.save()
        cart.discount_total += discount
        cart.gross_total += gross
        cart.net_total += gross - discount
        cart.save()

        items = CartItem.objects.filter(cart=cart)

        return render(request, 'cart/index-ajax.html', {'cart': cart, 'items': items})
    else: 
        return Http404

def remove_item(request):
    item_id = request.POST.get('cart', None)
    if request.is_ajax() and item_id: 
        cart = get_cart(request)

        item = get_object_or_404(CartItem, id=item_id)

        try:
            gross_total = item.gross_total
            discount_total = item.discount_total
            net_total = item.net_total
            item.delete()
            cart.discount_total -= discount_total
            cart.gross_total -= gross_total
            cart.net_total -= net_total
            cart.save()
             
        except IntegrityError:
            return JsonResponse({'success': False})
            
        return JsonResponse({'success': True})
    else:
        raise Http404
