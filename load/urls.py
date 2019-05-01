from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from load.api.viewsets import LoadViewSet
from . import views

app_name = 'load'

router = routers.DefaultRouter()
router.register(r'loads', LoadViewSet, base_name='api')

urlpatterns = [
    path('api/', include(router.urls)),
    path('loads/', views.list_loads, name='loads'),
    path('create/', views.LoadCreateView.as_view(), name='create-load'),
    path('<int:pk>/update/', views.LoadUpdateView.as_view(), name='update-load'),
    path('<int:pk>/accept/', views.accept_load, name='accept-load'),
    path('<int:pk>/reject/', views.reject_load, name='reject-load'),
    path('<int:pk>/drop/', views.drop_load, name='drop-load')
]
