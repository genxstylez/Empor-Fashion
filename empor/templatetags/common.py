from django import template
from django.template.loader import render_to_string
from product.models import Brand, Category

register = template.Library()

@register.simple_tag
def menu(request):
    categories = Category.objects.filter(parent=None)
    mbrands = Brand.objects.filter(category=1)
    wbrands = Brand.objects.filter(category=2)

    return render_to_string('empor/menu.html', {'categories': categories, 'mbrands': mbrands, 'wbrands': wbrands})
