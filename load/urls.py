from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include
from load.api.viewsets import LoadViewSet, CarrierLoadViewSet

app_name = 'load'

router = routers.DefaultRouter()
router.register(r'', LoadViewSet, base_name='load')
router.register('carrier', CarrierLoadViewSet, base_name='load')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.list_loads, name='loads'),
    path('create/', views.LoadCreateView.as_view(), name='create-load'),
    path('update/<int:pk>/', views.LoadUpdateView.as_view(), name='update-load'),
]
