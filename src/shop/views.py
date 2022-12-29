from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from shop.models import Product, Category
from cart.forms import CartAddProductForm
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': products})

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


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
    slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
    'shop/product/detail.html',
    {'product': product,
    'cart_product_form': cart_product_form,})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        context['cart_product_form'] = CartAddProductForm
        return context