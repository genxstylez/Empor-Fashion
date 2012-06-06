from django.shortcuts import render
from product.models import Product, Brand, Category

def index(request):
    products = Product.objects.filter(featured=True)
    brands = Brand.objects.all()
    categories = Category.objects.filter(parent=None)
    box_class = ['a11', 'a12', 'a21', 'a22']
    return render(request, 'empor/index.html', {'products': products, 'brands': brands, 'categories': categories, 'box_class': box_class })

