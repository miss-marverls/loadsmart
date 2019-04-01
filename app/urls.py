from django.urls import path

from . import views


app_name = 'app'

urlpatterns = [
    path(r'', views.index, name='index'),
]