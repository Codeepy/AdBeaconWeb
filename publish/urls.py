__author__ = 'dumbastic'

from django.conf.urls import url
from publish import views

urlpatterns = [
    url(r'^$', views.index, name='register'),
    url(r'^account/(?P<id>\d)', views.account, name='account'),
    url(r'^advertisement/', views.makeAdvs, name='imageupload'),
]