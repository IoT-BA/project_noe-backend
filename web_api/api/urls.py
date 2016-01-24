from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^batch/([0-9]+)/([0-9]+)/?$', views.batch, name='batch'),
    url(r'^last/([0-9]+)/([0-9]+)/?$', views.last, name='last'),
    url(r'^last/all/?$', views.last_all_nodes, name='last'),
]
