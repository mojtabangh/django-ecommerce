from django import forms
from orders.models import Order, OrderItem

class OrderCreateForm(forms.Form):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
        'postal_code', 'city']