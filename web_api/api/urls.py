from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^node/(.+)/?$', views.node_info),
    url(r'^points/save/?$', views.save_point),
    url(r'^points/([0-9a-z]+)/([0-9]+)/?$', views.points_this_node_key),
    url(r'^points/([0-9a-z]+)/?$', views.points_this_node),
    url(r'^points/all/([0-9]+)/?$', views.points_all_nodes_key),
    url(r'^points/all/?$', views.points_all_nodes),
    url(r'^rawpoints/([0-9a-z]+)/?$', views.rawpoints_this_node),
    url(r'^rawpoints/?$', views.rawpoints),
    url(r'^gis/?$', views.gis),
]
