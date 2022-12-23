from django.shortcuts import render, redirect
from django.urls import reverse

from orders.models import OrderItem
from orders.forms import OrderCreateForm
from orders.tasks import order_created
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],)
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # Set the order in the session
            request.session['order_id'] = order.id
            # Redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
    'orders/order/create.html',
    {'cart': cart, 'form': form})