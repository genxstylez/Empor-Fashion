from cart.models import ArchivedCart, ArchivedCartItem

def archive_cart(cart):
    Acart = ArchivedCart()
    Acart.user = cart.user
    Acart.session = cart.session
    Acart.total = cart.total
    Acart.created_at = cart.created_at
    Acart.last_modified = cart.last_modified
    Acart.save()

    for item in cart.items.all():
        ACitem = ArchivedCartItem()
        ACitem.product = item.product
        ACitem.quantity = item.quantity
        ACitem.total = item.total
        ACitem.cart = Acart
        ACitem.discount = item.discount
        ACitem.created_at = item.created_at
        ACitem.last_modified = item.last_modified
        ACitem.save()

    cart.delete()

    return Acart
