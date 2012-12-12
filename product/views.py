# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from empor.shortcuts import JsonResponse
from product.models import Product, Gender, Brand, Category

def brands(request):
    brands = Brand.objects.all()
    if request.is_ajax():
        return render(request, 'product/brands-ajax.html', {'brands': brands})
    return render(request, 'product/brands.html', {'brands': brands})

def brand(request, brand_slug):
    brand = Brand.objects.get(slug=brand_slug) 
    products = Product.on_site.filter(brand=brand)
    box_class = ['a11', 'a12', 'a21']
    return render(request, 'product/brand.html', {'brand': brand, 'products': products, 'box_class': box_class, 'popup': True})

def brand_products(request, brand_slug, gender_type=None, category=None):
    brand = Brand.objects.get(slug=brand_slug)
    if gender_type:
        gender = Gender.objects.get(name=gender_type)
        products = Product.on_site.filter(gender=gender, brand=brand)
        if category:
            category = Category.objects.get(id=category)
            products = products.filter(category=category)
    else:
        products = Product.on_site.filter(brand=brand)
    box_class = ['a11', 'a12', 'a21']
    return render(request, 'product/brand-products.html', {
		'products': products, 
		'box_class': box_class, 
		'brand': brand, 
		'category_id':category, 
		'gender': gender_type
	})

def gender_products(request, gender_type, category=None):
    gender = Gender.objects.get(name=gender_type)
    products = Product.on_site.filter(gender=gender)
    if category:
        category = Category.objects.get(id=category)
        products = products.filter(category=category)
    brands = Brand.objects.all()
    box_class = ['a11', 'a12', 'a21']
    return render(request, 'product/gender-products.html', {
        'products': products, 
        'box_class': box_class, 
        'gender': gender, 
        'brands': brands, 
        'category': category
    })

def product_view(request, brand_slug, gender_type, product_slug, category=None):
    gender = Gender.objects.get(name=gender_type)
    try:
        focus_product = Product.on_site.prefetch_related('brand', 'option_group').get(brand__slug=brand_slug, slug=product_slug)
    except Product.DoesNotExist:
        raise Http404

    products = Product.on_site.filter(brand__slug=brand_slug, gender=gender).prefetch_related('brand', 'option_group')

    if category:
        products.filter(category=category)

    box_class = ['a11', 'a12', 'a21']

    return render(request, 'product/product.html', {
        'products': products, 
        'focus_product': focus_product, 
        'box_class': box_class, 
        'popup': True,
        'brand': focus_product.brand
    })

def _check_stock(request):
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('product_id', None)
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            if product.stock > 0 :
                message = _('This item is available!')
                return JsonResponse({'success': True, 'message': message, 'item_count': product.stock})
            else:
                message = _('This item has sold out')
                return JsonResponse({'success': False, 'message': message})
    raise Http404
