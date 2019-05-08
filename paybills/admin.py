from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.BasicItem)
admin.site.register(models.PaymentProcess)
admin.site.register(models.PaymentSuccess)
admin.site.register(models.SubscriptionProcess)
admin.site.register(models.SubscriptionSuccess)
admin.site.register(models.SubscriptionPayment)




