from cart.models import ArchivedCart, ArchivedCartItem, CartItem

def archive_cart(cart):
    Acart = ArchivedCart()
    Acart.user = cart.user
    Acart.session = cart.session
    Acart.discount_total = cart.discount_total
    Acart.total = cart.total
    Acart.created_at = cart.created_at
    Acart.last_modified = cart.last_modified
    Acart.save()

    items = CartItem.objects.filter(cart=cart)

    for item in items:
        ACitem = ArchivedCartItem()
        ACitem.product = item.product
        ACitem.archived_cart = Acart
        ACitem.quantity = item.quantity
        ACitem.discount_total = item.discount_total
        ACitem.total = item.total
        ACitem.created_at = item.created_at
        ACitem.last_modified = item.last_modified
        ACitem.save()

    cart.delete()

    return Acart
