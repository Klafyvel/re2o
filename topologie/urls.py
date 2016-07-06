from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_switch/$', views.new_switch, name='new-switch'),
    url(r'^switch/(?P<switch_id>[0-9]+)$', views.index_port, name='index-port'),
    url(r'^edit_port/(?P<port_id>[0-9]+)$', views.edit_port, name='edit-port'),
    url(r'^new_port/(?P<switch_id>[0-9]+)$', views.new_port, name='new-port'),
    url(r'^edit_switch/(?P<switch_id>[0-9]+)$', views.edit_switch, name='edit-switch'),
]

