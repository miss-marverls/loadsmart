from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ShipperCreationForm, CarrierCreationForm
from .models import Shipper, Carrier


class ShipperRegistrationView(CreateView):
    """
    View that handles Shipper registration.
    """

    form_class = ShipperCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        """
        Overrides CreateView method post to include the creation of a Shipper when a User is created.

        :param django.http.HttpRequest request: Received request.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: If form is valid, redirects to login page. If form is not valid, remains in the registration.
        """

        form = ShipperRegistrationView.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_shipper = True
            user.save()

            shipper = Shipper.objects.create(user=user)
            shipper.save()

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class CarrierRegistrationView(CreateView):
    """
    View that handles Carrier registration.
    """

    form_class = CarrierCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        """
        Overrides CreateView method post to include the creation of a Carrier when a User is created.

        :param django.http.HttpRequest request: Received request.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: If form is valid, redirects to login page. If form is not valid, remains in the registration.
        """

        form = CarrierRegistrationView.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            mc_number = form.cleaned_data['mc_number']
            user.mc_number = mc_number
            user.is_carrier = True
            user.save()

            carrier = Carrier.objects.create(user=user, mc_number=mc_number)
            carrier.save()

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})
