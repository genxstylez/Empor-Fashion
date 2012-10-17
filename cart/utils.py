from cart.models import ArchivedCart, ArchivedCartItem, CartItem

def archive_cart(cart, revert=None):
    items = CartItem.objects.filter(cart=cart)
    if items:
        Acart = ArchivedCart()
        Acart.user = cart.user
        Acart.session = cart.session
        Acart.discount_total = cart.discount_total
        Acart.gross_total= cart.gross_total
        Acart.net_total = cart.net_total
        Acart.created_at = cart.created_at
        Acart.last_modified = cart.last_modified
        if revert:
            Acart.type = 1

        Acart.save()

        
        for item in items:
            ACitem = ArchivedCartItem()
            ACitem.product = item.product
            ACitem.archived_cart = Acart
            ACitem.quantity = item.quantity
            if revert:
                item.product.stock += item.quantity
                item.product.save()
            ACitem.discount_total = item.discount_total
            ACitem.gross_total = item.gross_total
            ACitem.net_total = item.net_total
            ACitem.created_at = item.created_at
            ACitem.last_modified = item.last_modified
            ACitem.save()

        cart.delete()
        return Acart

    cart.delete()
