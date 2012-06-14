from product.models import Brand, Category, Product, ProductImage, \
Collection, OptionGroup, Option, Gender
from django.contrib import admin

admin.site.register(Brand)
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(ProductImage)
admin.site.register(OptionGroup)
admin.site.register(Option)
