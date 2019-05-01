from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from users.models import Carrier, Shipper
from . import utils
from .decorators import shipper_required, carrier_required, login_required
from .forms import LoadForm, LoadEditRateForm
from .models import Load


@method_decorator(shipper_required, name='dispatch')
class LoadCreateView(BSModalCreateView):
    """
    View that handles the creation of a load.

    Only a Shipper can create a load.
    """

    template_name = 'load/new_load.html'
    form_class = LoadForm
    success_message = 'Success: Load was created.'
    success_url = reverse_lazy('load:loads')

    def form_valid(self, form):
        """
        Overrides form_valid method to automatically fill out the fields carrier, carrier_price, and shipper.
        """

        load = form.save(commit=False)
        load.carrier = None
        load.carrier_price = utils.calculate_carrier_price(load.shipper_price)
        if self.request.user.is_authenticated:
            shipper = Shipper.objects.get_shipper(self.request)
            load.shipper = shipper
        load.save()

        return super(LoadCreateView, self).form_valid(form)


@method_decorator(shipper_required, name='dispatch')
class LoadUpdateView(BSModalUpdateView):
    """
    View for load rate update.

    Only Shippers are allowed to change the load rate and they can only update their on loads.
    """

    model = Load
    template_name = 'load/edit_rate.html'
    form_class = LoadEditRateForm
    success_message = 'Success: Rate was updated.'
    success_url = reverse_lazy('load:loads')

    def form_valid(self, form):
        """
        Overrides form_valid method to automatically fill out the fields carrier, carrier_price, and shipper.
        """

        load = form.save(commit=False)
        load.carrier = None
        if self.request.user.is_authenticated:
            shipper = Shipper.objects.get_shipper(self.request)
            load.shipper = shipper
            load.carrier_price = utils.calculate_carrier_price(load.shipper_price)
        load.save()
        return super(LoadUpdateView, self).form_valid(form)


@login_required
def list_loads(request):
    """View that list the loads.

    The loads lists are different for Shippers and Carriers. These lists are available for logged users only.

    :param django.http.HttpRequest request: Received request.
    :return: The page with the list of loads for the Shipper or for the Carrier, depending on the User type.
    :rtype: django.http.HttpResponse
    """

    if request.user.is_shipper:
        return list_shipper_loads(request)
    return list_carrier_loads(request)


@shipper_required
def list_shipper_loads(request):
    """
    Lists the available and accepted loads of the Shipper.

    :param django.http.HttpRequest request: Received request.
    :return: The page with the list of loads for the Shipper.
    :rtype: django.http.HttpResponse
    """

    available_loads = Load.objects.get_shipper_available_loads(request)
    accepted_loads = Load.objects.get_shipper_accepted_loads(request)
    return render(request, 'load/shipper_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


@carrier_required
def list_carrier_loads(request):
    """
    Lists the all the available loads (from all Shippers) and the accepted loads of the Carrier.

    :param django.http.HttpRequest request: Received request.
    :return: The page with the list of loads for the Carrier.
    :rtype: django.http.HttpResponse
    """

    available_loads = Load.objects.get_carrier_available_loads(request)
    accepted_loads = Load.objects.get_carrier_accepted_loads(request)
    return render(request, 'load/carrier_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


@carrier_required
def accept_load(request, pk):
    """
    Accepts an available load.

    Only Carriers can accept an available load. When the load is accepted the Carrier that accepted it
    is added to the load field "carrier".

    :param django.http.HttpRequest request: Received request.
    :param pk: Load primary key
    :return: Carrier loads list page
    :rtype: django.http.HttpResponseRedirect
    """

    load = get_object_or_404(Load, pk=pk, carrier=None)
    carrier = Carrier.objects.get_carrier(request)
    load.carrier = carrier
    load.save()
    return redirect('load:loads')


@carrier_required
def reject_load(request, pk):
    """
    Rejects an available load.

    Only Carriers can reject an available load. When the load is rejected the Carrier who rejected it
    is added to the load field "dropped_by". The load remains available, except for the Carrier who rejected it.

    :param django.http.HttpRequest request: Received request.
    :param pk: Load primary key
    :return: Carrier loads list page
    :rtype: django.http.HttpResponseRedirect
    """

    load = get_object_or_404(Load, pk=pk, carrier=None)
    carrier = Carrier.objects.get_carrier(request)
    load.dropped_by.add(carrier)
    return redirect('load:loads')


@carrier_required
def drop_load(request, pk):
    """
    Drops an accepted load.

    Only Carriers can drop an accepted load. When the load is dropped the Carrier who dropped it
    is removed to the load field "carrier". The load becomes available again, except for the Carrier who dropped it.

    :param django.http.HttpRequest request: Received request.
    :param pk: Load primary key
    :return: Carrier loads list page
    :rtype: django.http.HttpResponseRedirect
    """

    carrier = Carrier.objects.get_carrier(request)
    load = get_object_or_404(Load, pk=pk, carrier=carrier)
    load.carrier = None
    load.save()
    load.dropped_by.add(carrier)
    return redirect('load:loads')
