from product.models import Brand, Category, Product, ProductImage, \
Collection, OptionGroup, Option, Gender, ProductThumb
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        return qs.filter(parent=None)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'small_width', 'small_height', 'medium_width', 'medium_height', 'large_width', 'large_height')

admin.site.register(Brand)
admin.site.register(Gender)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductThumb)
admin.site.register(OptionGroup)
admin.site.register(Option)
