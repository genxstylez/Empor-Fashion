from django.utils.translation import ugettext as _
from django.shortcuts import render
from product.forms import ProductForm

def index(request):
    return render('something')

def create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    return render(request, 'admin/create.html', {'form': form})

