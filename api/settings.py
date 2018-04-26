# -*- mode: python; coding: utf-8 -*-
# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
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

"""api.settings
Django settings specific to the API.
"""

# RestFramework config for API
REST_FRAMEWORK = {
    'URL_FIELD_NAME': 'api_url',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.DefaultACLPermission',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

# API permission settings
API_CONTENT_TYPE_APP_LABEL = 'api'
API_CONTENT_TYPE_MODEL = 'api'
API_PERMISSION_NAME = 'Can use the API'
API_PERMISSION_CODENAME = 'use_api'

# Activate token authentication
API_APPS = (
    'rest_framework.authtoken',
)
API_TOKEN_DURATION = 86400 # 24 hours
