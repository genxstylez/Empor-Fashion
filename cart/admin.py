from django.contrib import admin
from cart.models import Cart, CartItem, ArchivedCart, ArchivedCartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ArchivedCart)
admin.site.register(ArchivedCartItem)
