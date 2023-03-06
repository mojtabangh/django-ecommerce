from django.urls import path
from .views import PaymentProcessView, PaymentDoneView, PaymentCanceledView

app_name = 'payment'

urlpatterns = [
    path('process/', PaymentProcessView.as_view(), name='process'),
    path('done/', PaymentDoneView.as_view(), name='done'),
    path('canceled/', PaymentCanceledView.as_view(), name='canceled'),
]