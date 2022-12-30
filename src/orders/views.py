from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View, CreateView

from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from orders.tasks import order_created
from cart.cart import Cart

class OrderCreateView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        form = OrderCreateForm
        return render(
            self.request,
            'orders/order/create.html',
            {'cart': cart, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        form = OrderCreateForm(self.request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # applying coupon
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            self.request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
    'admin/orders/order/detail.html',
    {'order': order})