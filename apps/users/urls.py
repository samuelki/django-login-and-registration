from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/register$', views.register),
    url(r'^users/login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout)
]