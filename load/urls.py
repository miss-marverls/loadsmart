from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include
from load.api.viewsets import LoadViewSet, CarrierLoadViewSet

app_name = 'load'

router = routers.DefaultRouter()
router.register(r'', LoadViewSet, base_name='shipper')
router.register('carrier', CarrierLoadViewSet, base_name='carrier')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.list_loads, name='loads'),
    path('carrier/', views.list_carrier_loads, name='carrier-loads'),
    path('create/', views.LoadCreateView.as_view(), name='create-load'),
    path('update/<int:pk>/', views.LoadUpdateView.as_view(), name='update-load'),
    path('accept/<int:pk>/', views.accept_load, name='accept-load')
]
