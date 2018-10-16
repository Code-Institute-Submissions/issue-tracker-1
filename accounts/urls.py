from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/edit/$', profile_edit, name='edit_profile'),
    url(r'^profile/upgrade/$', profile_upgrade, name='profile_upgrade'),
    url(r'^profile/credits/$', add_credits, name='add_credits'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
]