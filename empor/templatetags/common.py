from django import template
from django.template.loader import render_to_string
from product.models import Brand, Category
from empor.settings import STATIC_URL

register = template.Library()

@register.simple_tag
def menu(request):
    categories = Category.objects.filter(parent=None)
    mbrands = Brand.objects.filter(categories=categories[0])
    wbrands = Brand.objects.filter(categories=categories[1])

    return render_to_string('empor/menu.html', {'categories': categories, 'mbrands': mbrands, 'wbrands': wbrands, 'STATIC_URL': STATIC_URL})
