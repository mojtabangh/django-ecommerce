from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView

from .models import Product, Category
from ecommerce.cart.forms import CartAddProductForm

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        category = None
        if self.kwargs.get('category_slug'):
            category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
            products = products.filter(category=category)
        context = {
            'products': products,
            'category': category,
            'categories': Category.objects.all(),
        }
        return render(request, 'shop/product/list.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        context['cart_product_form'] = CartAddProductForm
        return context