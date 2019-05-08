from django.conf.urls import url, include
from . import views

app_name = 'paybills'
urlpatterns = [
    url(r'^paypal-ipn/', views.PayPalIPN.as_view(), name='paypal-ipn'),
]








