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

"""
Django settings for re2o project.

Generated by 'django-admin startproject' using Django 1.8.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from __future__ import unicode_literals

import os
from .settings_local import *

# The root directory for the project
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Auth definition
PASSWORD_HASHERS = (
    're2o.login.SSHAPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)
AUTH_USER_MODEL = 'users.User'  # The class to use for authentication
LOGIN_URL = '/login/'           # The URL for login page
LOGIN_REDIRECT_URL = '/'        # The URL for redirecting after login

# Application definition
DJANGO_CONTRIB_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
EXTERNAL_CONTRIB_APPS = (
    'bootstrap3',
    'rest_framework',
    'reversion',
)
LOCAL_APPS = (
    'users',
    'machines',
    'cotisations',
    'topologie',
    'search',
    're2o',
    'preferences',
    'logs',
    'api',
)
INSTALLED_APPS = (
    DJANGO_CONTRIB_APPS +
    EXTERNAL_CONTRIB_APPS +
    LOCAL_APPS +
    OPTIONNAL_APPS
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

# The root url module to define the project URLs
ROOT_URLCONF = 're2o.urls'

# The templates configuration (see Django documentation)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Use only absolute paths with '/' delimiters even on Windows
            os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                're2o.context_processors.context_user',
            ],
        },
    },
]

# The WSGI module to use in a server environment
WSGI_APPLICATION = 're2o.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
# Proritary location search for translations
# then searches in {app}/locale/ for app in INSTALLED_APPS
# Use only absolute paths with '/' delimiters even on Windows
LOCALE_PATHS = [
    # For translations outside of apps
    os.path.join(BASE_DIR, 'templates', 'locale').replace('\\', '/')
]

# Should use time zone ?
USE_TZ = True

# Router config for database
DATABASE_ROUTERS = ['ldapdb.router.Router']

# django-bootstrap3 config
BOOTSTRAP3 = {
    'jquery_url': '/static/js/jquery-2.2.4.min.js',
    'base_url': '/static/bootstrap/',
    'include_jquery': True,
}
BOOTSTRAP_BASE_URL = '/static/bootstrap/'

# Directories where collectstatic should look for static files
# Use only absolute paths with '/' delimiters even on Windows
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
)
# Directory where the static files served by the server are stored
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
# The URL to access the static files
STATIC_URL = '/static/'
# Directory where the media files served by the server are stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
# The URL to access the static files
MEDIA_URL = '/media/'

# Models to use for graphs
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}
