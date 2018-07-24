from django.conf.urls import url
from . import views          


urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^createpost$', views.createpost),
    url(r'^create3$', views.create3),
    url(r'^login$', views.login),
    url(r'^logged$', views.logged),
    url(r'^goback$', views.logged),
    url(r'^logout$', views.logout),
    url(r'^viewitem/(?P<id>\w+)$', views.viewitem),
    url(r'^delete$', views.delete),
    url(r'^edit/(?P<id>\w+)$', views.edit),
    url(r'^update/(?P<id>\w+)$', views.update),

]                            