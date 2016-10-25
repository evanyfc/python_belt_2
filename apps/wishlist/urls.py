from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add$', add, name='add'),
    url(r'^create$', create, name='create'),
    url(r'^show/(?P<id>\d+)$', show, name='show'),
    url(r'^delete/(?P<id>\d+)$', delete, name='delete'),
    url(r'^join/(?P<id>\d+)$', join, name='join'),
    url(r'^unjoin/(?P<id>\d+)$', unjoin, name='unjoin'),
]
