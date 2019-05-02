from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register_shipper/', views.ShipperRegistrationView.as_view(),
         name='register_shipper'),
    path('register_carrier/', views.CarrierRegistrationView.as_view(),
         name='register_carrier'),
    path('token/', obtain_auth_token),

]
