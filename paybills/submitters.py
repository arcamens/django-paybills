from django.urls import reverse
from django.conf import settings
from html import escape
from . import models
import time
import hmac


class PayPalForm:
    def __init__(self, user, item, payload):
        PAYPAL_IPN_URL = '%s%s' % (settings.PAYPAL_IPN_DOMAIN, 
        reverse(settings.PAYPAL_IPN_VIEW))
        
        payload.update({
        'notify_url': PAYPAL_IPN_URL,  
        'bn': settings.PAYPAL_BUSINESS_NAME,
        'business': settings.PAYPAL_ID, })
        print('notify_url:', payload['notify_url'])
        self.payload = payload

    def __str__(self):
        param  = '<input type="hidden" name="%s" value="%s"/>'
        fmt    = lambda key, value: param % (escape(key), escape(value))
        action = (settings.PAYPAL_URL , "/cgi-bin/webscr")
        hidden = '\n'.join([fmt(ind[0], str(ind[1])) 
        for ind in self.payload.items()])

        html = ("<meta charset='utf-8' />",
        "<p>Redirecting...</p>",
        '<form method="post" action="%s%s">' % action,
         hidden, "</form>",
        "<script>document.forms[0].submit()</script>")
        return '\n'.join(html)

    def encode_id(self, id):
        key = hmac.new(settings.SECRET_KEY.encode(), 
        ('payid ' + str(id)).encode()).hexdigest()

        return settings.PAYMENTS_REALM + ' ' + str(id) + ' ' + key

class ManualForm(PayPalForm):
    def __init__(self, user, item, payload):
        record = models.PaymentProcess.objects.create(
        user=user, item=item)

        payload.update({
        'invoice': '%s-1' % self.encode_id(record.id + time.time()), 
        'custom': record.id, 
        'cmd': '_xclick'})

        super(ManualForm, self).__init__(user, item, payload)

class SubscriptionForm(PayPalForm):
    def __init__(self, user, item, payload):
        record = models.SubscriptionProcess.objects.create(
        user=user, item=item)

        payload.update({
        'invoice': '%s-1' % self.encode_id(record.id + time.time()), 
        'custom': record.id, 
        'cmd': '_xclick-subscriptions'})

        super(SubscriptionForm, self).__init__(user, item, payload)








