# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product
from cart.models import Cart, CartItem
from cart.utils import archive_cart

def get_cart(request):
    if 'session_key' not in request.session:
        request.session.save()
    if 'cart' in request.session:
        cart = request.session['cart']
        if request.user.is_authenticated():
            if Cart.objects.filter(user=request.user) and cart != request.user.cart:
                archive_cart(request.user.cart, 'expired')
            cart.user = request.user
            cart.save()
    else:
        if request.user.is_authenticated():
            cart, created  = Cart.objects.get_or_create(user=request.user)
        else:
            cart, created = Cart.objects.get_or_create(session=request.session.session_key)

    if cart.items.count() == 0:
        cart.net_total = 0
        cart.save()
    request.session['cart'] = cart

    return cart

def index(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/index.html', {'cart': cart, 'items': items})

def add_item(request):
    product_id = request.POST.get('product_id', None)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST' and request.is_ajax():

        if product.has_options and product.parent == None:
            return JsonResponse({'message': _('Please choose a size')})

        cart = get_cart(request)
        quantity = request.POST.get('quantity')
        if not quantity:
            quantity = 1
        quantity = int(quantity)

        if product.stock >= quantity:
            try:
                item = CartItem.objects.get(product=product, cart=cart)
            except CartItem.DoesNotExist:
                item = CartItem()
                item.cart = cart
                item.product = product

            discount = 0
            if product.discountable:
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

            product.stock -= quantity
            product.save()

            items = CartItem.objects.filter(cart=cart)

            return render(request, 'cart/index-ajax.html', {'cart': cart, 'items': items})
    return JsonResponse({'message': _('This item has sold out')})

def remove_item(request):
    item_id = request.POST.get('cart', None)
    if request.is_ajax() and item_id: 
        cart = get_cart(request)

        item = get_object_or_404(CartItem, id=item_id)

        try:
            gross_total = item.gross_total
            discount_total = item.discount_total
            net_total = item.net_total
            item.product.stock += item.quantity
            item.product.save()
            item.delete()
            cart.discount_total -= discount_total
            cart.gross_total -= gross_total
            cart.net_total -= net_total
            cart.save()

            request.session['cart'] = cart

        except IntegrityError:
            return JsonResponse({'success': False})
            
        return JsonResponse({'success': True, 'gross_total': cart.gross_total, 'discount_total': cart.discount_total, 'net_total': cart.net_total})

    raise Http404
