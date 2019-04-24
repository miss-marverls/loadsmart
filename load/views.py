from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Load
from users.models import Carrier
from .forms import LoadForm, LoadEditRateForm
from .decorators import shipper_required, carrier_required, login_required
from django.utils.decorators import method_decorator
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from . import utils


# Create your views here.
@method_decorator(shipper_required, name='dispatch')
class LoadCreateView(BSModalCreateView):
    template_name = 'load/new_load.html'
    form_class = LoadForm
    success_message = 'Success: Load was created.'
    success_url = reverse_lazy('load:loads')

    def form_valid(self, form):
        load = form.save(commit=False)
        load.carrier = None
        load.carrier_price = utils.calculate_carrier_price(load.shipper_price)
        if self.request.user.is_authenticated:
            load.shipper = self.request.user
        load.save()
        return super(LoadCreateView, self).form_valid(form)


@method_decorator(shipper_required, name='dispatch')
class LoadUpdateView(BSModalUpdateView):
    model = Load
    template_name = 'load/edit_rate.html'
    form_class = LoadEditRateForm
    success_message = 'Success: Rate was updated.'
    success_url = reverse_lazy('load:loads')

    def form_valid(self, form):
        load = form.save(commit=False)
        load.carrier = None
        if self.request.user.is_authenticated:
            load.shipper = self.request.user
            load.carrier_price = utils.calculate_carrier_price(load.shipper_price)
        load.save()
        return super(LoadUpdateView, self).form_valid(form)

@login_required
def list_loads(request):
    if request.user.is_shipper:
        return list_shipper_loads(request)
    return list_carrier_loads(request)


@shipper_required
def list_shipper_loads(request):
    available_loads = Load.objects.filter(carrier=None, shipper_id=request.user.pk)
    accepted_loads = Load.objects.exclude(carrier=None).filter(shipper_id=request.user.pk)
    return render(request, 'load/shipper_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


@carrier_required
def list_carrier_loads(request):
    carrier = Carrier.objects.get(user=request.user.pk)
    dropped_loads = carrier.dropped_by.all()
    available_loads = Load.objects.filter(
        carrier=None).exclude(id__in=dropped_loads)
    accepted_loads = Load.objects.filter(carrier=carrier)
    return render(request, 'load/carrier_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


@carrier_required
def accept_load(request, pk):
    load = get_object_or_404(Load, pk=pk, carrier=None)
    carrier = Carrier.objects.get(user=request.user.pk)
    load.carrier = carrier
    load.save()
    return redirect('load:loads')


@carrier_required
def drop_load(request, pk):
    load = get_object_or_404(Load, pk=pk, carrier=None)
    carrier = Carrier.objects.get(user=request.user.pk)
    load.dropped_by.add(carrier)
    return redirect('load:loads')
