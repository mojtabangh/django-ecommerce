from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm

class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        form = CartAddProductForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override']
            )
        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={
                    'quantity': item['quantity'],
                    'override': True
                }
            )
        context['cart'] = cart
        context['coupon_apply_form'] = CouponApplyForm()
        return context