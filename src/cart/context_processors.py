from .cart import Cart

def cart():
    return {'cart': Cart(request),}