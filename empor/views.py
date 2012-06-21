from django.shortcuts import render
from django.conf import settings
from product.models import Product

def index(request):

    if settings.DEBUG == True:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(featured=True)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'empor/index.html', {'products': products, 'box_class': box_class })

