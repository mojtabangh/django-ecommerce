from django.urls import path

from coupons.views import coupon_apply

app_name = 'coupons'

urlpatterns = [
    path('apply/', coupon_apply, name='apply'),
]