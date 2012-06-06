# -*- coding: utf-8 -*-
from django.shortcuts import render
from product.models import Product

def product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    group = product.product_group
    return render(request, 'product/site/product.html', {'product': product, 'group': group})
