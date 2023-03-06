from django.urls import path
from cart.views import CartDetailView, CartAddView, CartRemoveView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
]