from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
# nas versões django 1.9.* essa importação era no django.core.urlresolvers

from .forms import CustomUserCreationForm


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

