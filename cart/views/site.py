from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product
from cart.models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated():
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session=request.session.session_key)
    return cart

def index(request):
    cart = get_cart(request)

    return render(request, 'cart/site/index.html', {'cart': cart})

def add_item(request):
    cart = get_cart(request)
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        product = get_object_or_404(Product, id=product_id)

        try:
            item = CartItem.objects.get(product=product, cart=cart)
            item.quantity += int(quantity)
            cart.total -= item.total
            item.total = int(product.price) * item.quantity
            item.save()
            cart.total += item.total
            cart.save()
        except CartItem.DoesNotExist:
            item = CartItem()
            item.cart = cart
            item.product = product
            item.quantity = quantity
            item.total = int(product.price) * int(quantity)
            item.save()
            cart.total += item.total
            cart.save()

        return JsonResponse({'success': True})

    else: 
        return Http404

def remove_item(request, item_id):
    cart = get_cart(request)

    item = get_object_or_404(CartItem, id=item_id)

    try:
        total = item.total
        item.delete()
        cart.total -= total
        cart.save()
         
    except IntegrityError:
        return JsonResponse({'success': False})
        
    return JsonResponse({'success': True})
