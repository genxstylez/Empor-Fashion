from cart.models import Cart
def cart_required(f):

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            Cart.objects.get_or_create(user=request.user)
        else:
            Cart.objects.get_or_create(session=request.session.session_key)

        return f(request, *args, **kwargs)

    return wrapper
                     
