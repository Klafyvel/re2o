"""re2o URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import index

urlpatterns = [
    url(r'^$', index),
    url('^logout/', auth_views.logout, {'next_page': '/'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^cotisations/', include('cotisations.urls')),
    url(r'^machines/', include('machines.urls')),
    url(r'^topologie/', include('topologie.urls')),
    url(r'^logs/', include('logs.urls')),
]
