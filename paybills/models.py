from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings

# Create your models here.

class BasicItem(models.Model):
    """
    Users should inherit from this class for modeling
    their products/items. Then users of this application
    could access their items with:

    basic_item.item_model_name.
    """

    # We need this because there are some products
    # that arent paid at all. We need logging scheme
    # for the products a given user has owned be it free
    # or not.
    user = models.ForeignKey(settings.PAYBILLS_USER, 
    null=False, on_delete=models.CASCADE, related_name='items')

    created  = models.DateTimeField(auto_now_add=True, null=True)

class BasicService(models.Model):
    """
    """

    # Users who had subscription sign up success.
    users = models.ManyToManyField(
    settings.PAYBILLS_USER, related_name='services', 
    symmetrical=False)

    created  = models.DateTimeField(auto_now_add=True, null=True)

class PaymentProcess(models.Model):
    """
    This record is created from ManualProcess view
    it yields information about the Item thats
    being purchased.
    """

    user = models.ForeignKey(settings.PAYBILLS_USER, 
    null=False, on_delete=models.CASCADE, related_name='manual_proceses')

    # A given payment process should be mapped to just
    # one item. It avoids misbehaviors.
    item = models.OneToOneField('BasicItem', null=False,
    on_delete=models.CASCADE, related_name='payment_process')

    created  = models.DateTimeField(auto_now_add=True, null=True)

class PaymentSuccess(models.Model):
    process = models.OneToOneField('PaymentProcess', 
    null=False, on_delete=models.CASCADE, related_name='success')

    created  = models.DateTimeField(auto_now_add=True, null=True)

class SubscriptionProcess(models.Model):
    """
    This table records all times an user
    starts a subscription process. 

    it is used by SubscriptionSuccess to check
    divergent information about the process.

    It is important to notice that for starting
    a subscription process it is necessary to have
    already an user account.
    """

    # An user can purchase multiple services.
    user = models.ForeignKey(settings.PAYBILLS_USER, 
    null=False, on_delete=models.CASCADE, related_name='subscription_processes')

    # An user should be subscribed just once to a service.
    service = models.OneToOneField('BasicService', 
    null=False, on_delete=models.CASCADE, related_name='subscription_processes')

    invoice_id = models.IntegerField(null=True, default=15)
    created  = models.DateTimeField(auto_now_add=True, null=True)

class SubscriptionSuccess(models.Model):
    """
    This table records all times the customer
    has subscribed and it was succesful.

    A customer may subscribe multiple times
    it should be logged here.
    """

    # A SubscriptionSuccess record is related to a 
    # SubscriptionProcess record.
    process = models.OneToOneField('SubscriptionProcess', 
    null=False, on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True, null=True)

class SubscriptionPayment(models.Model):
    """
    These records are payments that were made
    from a given subscription process.
    """

    process = models.ForeignKey('SubscriptionProcess', 
    null=False, on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True, null=True)

class UnsubscriptionSuccess(models.Model):
    process = models.OneToOneField('SubscriptionSuccess', 
    null=False, on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True, null=True)





