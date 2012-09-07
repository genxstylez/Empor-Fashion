from product.models import Brand, Category, Product, ProductImage, \
Collection, OptionGroup, Option, Gender, ProductThumb
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        return qs.filter(parent=None)

admin.site.register(Brand)
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection)
admin.site.register(ProductImage)
admin.site.register(ProductThumb)
admin.site.register(OptionGroup)
admin.site.register(Option)
