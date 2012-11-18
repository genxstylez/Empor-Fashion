# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from Product import Category, Brand

register = template.Library()

@register.simple_tag
def gender_nav(gender):
    categories = Category.objects.filter(gender=gender)
    brands = Brand.objects.filter(gender=gender)

    return render_to_string('product/gender_nav.html', {'categories': categories, 'brands': brands, 'gender': gender})

@register.simple_tag
def brand_nav(brand):
    men_categories = Category.objects.filter(brand=brand, gender__id=1)
    women_categories = Category.objects.filter(brand=brand, gender__id=2)
    
    return render_to_string('product/brand_nav.html', {'men_categories': men_categories, 'women_categories': women_categories, 'brand': brand})
