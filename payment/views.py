import braintree

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View, TemplateView

from orders.models import Order

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

class PaymentProcessView(View):
    order_id = None
    order = None
    total_cost = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.order_id = self.request.session.get('order_id')
        self.order = get_object_or_404(Order, id=self.order_id)
        self.total_cost = self.order.get_total_cost()

    def post(self, request, *args, **kwargs):
        # retrieve nonce
        nonce = self.request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{self.total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order aS paid
            self.order.paid = True
            # store the unique transaction id
            self.order.braintree_id = result.transaction.id
            self.order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    def get(self, request, *args, **kwargs):
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            self.request,
            'payment/process.html',
            {
                'order': self.order,
                'client_token': client_token
            }
        )


class PaymentDoneView(TemplateView):
    template_name = 'payment/done.html'


class PaymentCanceledView(TemplateView):
    template_name = 'payment/canceled.html'