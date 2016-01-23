from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get/([0-9]+)/([0-9]+)/?$', views.get, name='get'),
]
