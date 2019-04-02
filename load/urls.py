from django.urls import path
from . import views

app_name = 'load'

urlpatterns = [
    path('new/', views.new_load, name='new_load'),
    path('', views.list_loads, name='loads'),
]
