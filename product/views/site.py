from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from product.models import Product

def product_view(request, product_id):
    products = Product.objects.all()
    focus_product = get_object_or_404(Product, id=product_id)
    box_class = ['a11', 'a12', 'a21', 'a22']

    return render(request, 'product/site/product.html', {'products': products, 'focus_product': focus_product, 'box_class': box_class })
    
