from django.urls import path
from payment.views import payment_process, payment_canceled, payment_done

app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='process'),
    path('done/', payment_done, name='done'),
    path('canceled/', payment_canceled, name='canceled'),
]