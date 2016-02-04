from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^points/([0-9]+)/?$', views.points_this_node),
    url(r'^points/all/?$', views.points_all_nodes),
    url(r'^points/([0-9]+)/([0-9]+)/?$', views.points_this_node_key),
    url(r'^node/([0-9]+)/?$', views.node_info),
]
