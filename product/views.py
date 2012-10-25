# -*- coding: utf-8 -*_
from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product, Gender

def products(request, gender_type=None):
    if gender_type:
        gender = Gender.objects.get(name=gender_type)
        products = Product.on_site.filter(gender=gender)
    else:
        products = Product.on_site.all()
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'product/products.html', {'products': products, 'box_class': box_class })

def product_view(request, brand_slug, product_slug):
    try:
        focus_product = Product.objects.prefetch_related('brand', 'option_group').get(brand__slug=brand_slug, slug=product_slug, parent=None)
    except Product.DoesNotExist:
        raise Http404

    products = Product.objects.filter(parent=None).prefetch_related('brand', 'option_group')
    box_class = ['a11', 'a12', 'a21', 'a22']

    return render(request, 'product/product.html', {'products': products, 'focus_product': focus_product, 'box_class': box_class, 'popup': True})

def _check_stock(request):
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('product_id', None)
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            if product.stock > 0 :
                message = _('This item is available!')
                return JsonResponse({'success': True, 'message': message})
            else:
                message = _('This item has sold out')
                return JsonResponse({'success': False, 'message': message})
    raise Http404
