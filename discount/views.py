from django.shortcuts import render
from discount.forms import DiscountForm

def index(request):
    form = DiscountForm(request.POST or None)

    return render(request, 'discount/index.html', {'form': form})
