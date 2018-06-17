# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2018  Mael Kervella
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""api.urls

Urls de l'api, pointant vers les fonctions de views
"""

from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    # Services
    url(r'^services/$', views.services),
    url(
        r'^services/(?P<server_name>\w+)/(?P<service_name>\w+)/regen/$',
        views.services_server_service_regen
    ),
    url(r'^services/(?P<server_name>\w+)/$', views.services_server),

    # DNS
    url(r'^dns/mac-ip-dns/$', views.dns_mac_ip_dns),
    url(r'^dns/alias/$', views.dns_alias),
    url(r'^dns/corresp/$', views.dns_corresp),
    url(r'^dns/mx/$', views.dns_mx),
    url(r'^dns/ns/$', views.dns_ns),
    url(r'^dns/txt/$', views.dns_txt),
    url(r'^dns/srv/$', views.dns_srv),
    url(r'^dns/zones/$', views.dns_zones),

    # Unifi controler AP names
    url(r'^unifi/ap_names/$', views.accesspoint_ip_dns),

    # Firewall
    url(r'^firewall/ouverture_ports/$', views.firewall_ouverture_ports),

    # DHCP
    url(r'^dhcp/mac-ip/$', views.dhcp_mac_ip),

    # Mailings
    url(r'^mailing/standard/$', views.mailing_standard),
    url(
        r'^mailing/standard/(?P<ml_name>\w+)/members/$',
        views.mailing_standard_ml_members
    ),
    url(r'^mailing/club/$', views.mailing_club),
    url(
        r'^mailing/club/(?P<ml_name>\w+)/members/$',
        views.mailing_club_ml_members
    ),
]