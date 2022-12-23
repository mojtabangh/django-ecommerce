from django.urls import path
from orders.views import order_create, admin_order_detail

app_name = 'orders'
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
]