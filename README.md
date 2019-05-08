# Django Paybills 

This package is a way to abstract and simplify the implementation of django platforms that interact with paypal. It turns out to be a
nap to receive payments and keep constraints on your platform resources/features. It accepts manual and subscription payments.

# Install

~~~
pip install django-paybills
~~~

### Setup

~~~
PAYMENTS_REALM = 'opus123'
PAYPAL_ID = 'CDA2QQH9TQ44C' #PayPal account ID` to `opus/settings.py`

PAYPAL_IPN_DOMAIN = 'http://opus.arcamens.com'
PAYPAL_IPN_DOMAIN = LOCAL_IP_ADDR if DEBUG else PAYPAL_IPN_DOMAIN

# The ipn view.
PAYPAL_IPN_VIEW   = 'site_app:paypal-ipn'
PAYPAL_BUSINESS_NAME = ''

~~~

# Donnate

Please visit the below url in case you find paybills useful.

https://url

# Instroduction

The django-paybill packages comes with a set of basic classes which should be inherited in your application.
It follows with a demo where you can donnate money to me :)

The basic classes are described below.

~~~python
class BasicItem(models.Model):
    """
    This class maps to the item that you're selling.
    """
    pass

class BasicService(models.Model):
    """
    In case you want subscription payments this class model
    your actual platform plans.
    """
    pass

~~~





