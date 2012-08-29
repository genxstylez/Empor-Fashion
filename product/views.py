from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render
from product.models import Product

def product_view(request, brand, product_slug):
    try:
        focus_product = Product.objects.prefetch_related('brand', 'option_group').get(brand__name=brand, slug=product_slug, parent=None)
    except Product.DoesNotExist:
        raise Http404

    if request.is_ajax():
        return render(request, 'product/product-ajax.html', {'focus_product': focus_product})
    
    products = Product.objects.all().prefetch_related('brand', 'option_group')
    box_class = ['a11', 'a12', 'a21', 'a22']

    return render(request, 'product/product.html', {'products': products, 'focus_product': focus_product, 'box_class': box_class, 'popup': True})
