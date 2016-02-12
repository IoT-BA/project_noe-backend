from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^points/([0-9]+)/?$', views.points_this_node),
    url(r'^points/all/?$', views.points_all_nodes),
    url(r'^points/all/([0-9]+)/?$', views.points_all_nodes_key),
    url(r'^points/([0-9]+)/([0-9]+)/?$', views.points_this_node_key),
    url(r'^node/([0-9]+)/?$', views.node_info),
    url(r'^points/save/?$', views.save_point),
    url(r'^rawpoints/?$', views.rawpoints),
    url(r'^gecko/funnel/([0-9]+)/?$', views.gecko_funnel_key),
    url(r'^gecko/line_datetime/([0-9]+)/([0-9]+)/?$', views.gecko_line_datetime_node_key),
    url(r'^gecko/meter/([0-9]+)/([0-9]+)/?$', views.gecko_meter_node_key),
]
