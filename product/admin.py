from django.utils.translation import ugettext as _
from product.models import Brand, Category, Product, ProductImage, \
Collection, OptionGroup, Option, Gender, ProductThumb
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        return qs.filter(parent=None)

class ProductImageAdmin(admin.ModelAdmin):
    actions = ['really_delete_selected']
    def get_actions(self, request):
        actions = super(ProductImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 ProductImage entry was"
        else:
            message_bit = "%s ProductImage entries were" % queryset.count()
        self.message_user(request, _("%s successfully deleted.") % message_bit)
    really_delete_selected.short_description = _("Delete selected entries")
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
