from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^bug', add_bug_upvote, name='bug_upvote'),
    url(r'^feature', add_feature_request_upvote, name='feature_upvote'),
]