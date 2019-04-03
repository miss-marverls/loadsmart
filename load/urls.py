from django.urls import path
from . import views

app_name = 'load'

urlpatterns = [
    path('', views.list_loads, name='loads'),
    path('create/', views.LoadCreateView.as_view(), name='create-load'),
]
