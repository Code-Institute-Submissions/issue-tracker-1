from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^upgrade$', subscription_purchase, name='subscription_purchase'),
    url(r'^credits$', credits_purchase, name='credits_purchase'),
]