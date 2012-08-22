from django.shortcuts import render
from django.conf import settings
from product.models import Product, Gender

def index(request):

    if settings.DEBUG == True:
        products = Product.objects.filter(parent=None)
    else:
        products = Product.objects.filter(featured=True)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'empor/index.html', {'products': products, 'box_class': box_class })

def gender(request, gender_type):   
    gender = Gender.objects.get(name=gender_type)
    if settings.DEBUG == True:
        products = gender.products.filter(parent=None)
    else:
        products = gender.products.filter(featured=True)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'empor/index.html', {'products': products, 'box_class': box_class })
