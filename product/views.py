from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render
from product.models import Product, Gender

def products(request, gender_type=None):
    if gender_type:
        gender = Gender.objects.get(name=gender_type)
        products = gender.products.filter(parent=None)
    else:
        products = Product.objects.filter(parent=None)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'product/products.html', {'products': products, 'box_class': box_class })

def product_view(request, brand_slug, product_slug):
    try:
        focus_product = Product.objects.prefetch_related('brand', 'option_group').get(brand__slug=brand_slug, slug=product_slug, parent=None)
    except Product.DoesNotExist:
        raise Http404

    if request.is_ajax():
        return render(request, 'product/product-ajax.html', {'focus_product': focus_product})
    
    products = Product.objects.filter(parent=None).prefetch_related('brand', 'option_group')
    box_class = ['a11', 'a12', 'a21', 'a22']

    return render(request, 'product/product.html', {'products': products, 'focus_product': focus_product, 'box_class': box_class, 'popup': True})
