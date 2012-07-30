from django.shortcuts import render
from discount.forms import DiscountForm

def index(request):
    form = DiscountForm(request.POST or None)
    if form.is_valid():
        discount = form.save(commit=False)
        for brand in discount.valid_brands.all():
            for product in brand.products.all():
                discount.valid_products = product.id
        discount.save_m2m()

    return render(request, 'discount/index.html', {'form': form})
