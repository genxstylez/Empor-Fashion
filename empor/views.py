from django.shortcuts import render
from product.models import Product

def index(request):
    products = Product.objects.filter(featured=True)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'empor/index.html', {'products': products, 'box_class': box_class })

