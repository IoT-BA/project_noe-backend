from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^gw/info/([0-9a-zA-Z]+)/?$', views.gw_info),
    url(r'^gw/register/([0-9a-zA-Z]+)/?$', views.gw_register),
    url(r'^node/([0-9a-zA-Z]+)/?$', views.node_info),
    url(r'^rssi/([0-9a-zA-Z]+)/?$', views.rssi_this_node),
    url(r'^user/([0-9a-zA-Z\._]+)/?$', views.user_info),
    url(r'^users/?$', views.users),
    url(r'^nodes/?$', views.nodes),
    url(r'^points/save/?$', views.save_point),
    url(r'^lorawan/save/?$', views.save_lorawanrawpoint),
    url(r'^lorawan/points/all/?$', views.lorawan_points_all),
    url(r'^points/([0-9a-zA-Z]+)/([0-9]+)/?$', views.points_this_node_key),
    url(r'^points/([0-9a-zA-Z]+)/?$', views.points_this_node),
    url(r'^points/all/([0-9]+)/?$', views.points_all_nodes_key),
    url(r'^points/all/?$', views.points_all_nodes),
    url(r'^rawpoints/save/?$', views.save_rawpoint),
    url(r'^rawpoints/([0-9a-zA-Z]+)/?$', views.rawpoints_this_node),
    url(r'^rawpoints/?$', views.rawpoints),
    url(r'^gis/?$', views.gis),
    url(r'^login/?$', views.user_login),
]
