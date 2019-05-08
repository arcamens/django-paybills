from paybills.submitters import ManualForm, SubscriptionForm
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from random import randint
from . import forms
from . import models
import requests

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class PayPalIPN(View):
    def post(self, request):
        print('PayPalIPN Details:%s' % request.POST)
        url = '%s/cgi-bin/webscr' % settings.PAYPAL_URL

        req = requests.post(url, 'cmd=_notify-validate&%s' % request.body.decode(
        request.POST.get('charset') or request.content_params['charset']),
        headers={'content-type': request.content_type})

        if req.text != 'VERIFIED':
            self.on_invalid_call(request.POST)
        else:
            self.on_valid_call(request.POST)
        return HttpResponse(status=200)
    
    def on_invalid_call(self, data):
        """    
        Hacker attempts/not validated ipn calls by paypal.
        """

        print('on_invalid_call:%s', data)

    def on_valid_call(self, data):
        map = {'web_accept': self.handle_web_accept,
        'recurring_payment': self.handle_recurring_payment,
        'subscr_payment': self.handle_recurring_payment,
        'subscr_cancel': self.handle_unsubscr_cancel,
        'subscr_signup': self.handle_subscr_signup}

        handle = map[data['txn_type']]
        handle(data)

    def handle_web_accept(self, data):
        """
        """

        record0 = models.PaymentProcess.objects.get(
        id=data['custom'])

        # Enable the user, it remains saving
        # information on the PaymentSuccess record.
        # I need to add more fields to it in order
        # to better log information.
        record1 = models.PaymentSuccess.objects.create(process=record0)
        self.on_manual_payment(data, record0.user, record0.item)
        self.on_success(data, record0.user, record0.item)

    def handle_recurring_payment(self, data):
        record0 = models.SubscriptionProcess.objects.get(
        id=data['custom'])

        record1, _ = models.SubscriptionSuccess.objects.get_or_create(
        process=record0)

        record2 = models.SubscriptionPayment.objects.create(process=record0)

        self.on_success(data, record0.user, record0.item)
        self.on_subscription_payment(data, record0.user, record0.item)

    def handle_subscr_signup(self, data):
        """
        """

        record0 = models.SubscriptionProcess.objects.get(
        id=data['custom'])

        record1 = models.SubscriptionSuccess.objects.get_or_create(process=record0)
        self.on_subscription_signup(data, record0.user, record0.item)

    def handle_unsubscr_cancel(self, data):
        record0 = models.SubscriptionProcess.objects.get(
        id=data['custom'])

        record1 = models.SubscriptionSuccess.objects.get(
        id=data['custom'])

        record1 = models.UnsubscriptionSuccess.objects.create(
        process=record0)

        self.on_subscription_cancel(data, record0.user, record0.item)

    def on_subscription_cancel(self, data, user, item):
        pass

    def on_subscription_signup(self, data, user, item):
        pass

    def on_manual_payment(self, data, user, item):
        pass

    def on_subscription_payment(self, data, user, item):
        pass

    def on_success(self, data, user, item):
        """
        Users should override this method to perform
        actions when payments are made.
        """
        pass





