from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
# nas versões django 1.9.* essa importação era no django.core.urlresolvers

from .models import Carrier
from .forms import ShipperCreationForm, CarrierCreationForm


class ShipperRegistrationView(CreateView):
    form_class = ShipperCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        form = ShipperRegistrationView.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_shipper = True
            user.save()

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class CarrierRegistrationView(CreateView):
    form_class = CarrierCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        form = CarrierRegistrationView.form_class(request.POST)
        print(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            mc_number = form.cleaned_data['mc_number']
            user.mc_number = mc_number
            user.is_carrier = True
            user.save()

            carrier = Carrier.objects.create(user=user, mc_number=mc_number)
            print(carrier)
            carrier.save()

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})
