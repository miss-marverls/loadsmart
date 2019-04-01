"""loadsmart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from load.api.viewsets import LoadViewSet
from load.views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register('load', LoadViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('load/register', register_load, name = 'register_load'),
    path('load/new', new_load, name = 'new_load'),
    path('create/', LoadCreateView.as_view(), name='create_load'),
    path('loads', list_loads, name = 'loads'),
    path('', include('app.urls', namespace='app')),
    path('users/', include('users.urls', namespace='users')),
]
