from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^create', add_comment, name='add_comment'),
]