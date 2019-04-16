from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Load
from users.models import Carrier
from .forms import LoadForm, LoadEditRateForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView


# Create your views here.
class LoadCreateView(BSModalCreateView):
    template_name = 'load/new_load.html'
    form_class = LoadForm
    success_message = 'Success: Load was created.'
    success_url = reverse_lazy('load:loads')

    def form_valid(self, form):
        load = form.save(commit=False)
        load.carrier = None
        if self.request.user.is_authenticated:
            load.shipper = self.request.user
        load.save()
        return super(LoadCreateView, self).form_valid(form)


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
        load.save()
        return super(LoadUpdateView, self).form_valid(form)


def list_loads(request):
    available_loads = Load.objects.filter(carrier=None)
    accepted_loads = Load.objects.exclude(carrier=None)
    return render(request, 'load/shipper_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


def list_carrier_loads(request):
    carrier = Carrier.objects.get(user=request.user.pk)
    dropped_loads = carrier.dropped_by.all()
    available_loads = Load.objects.filter(carrier=None).exclude(id__in=dropped_loads)
    accepted_loads = Load.objects.filter(carrier=carrier)
    return render(request, 'load/carrier_load_list.html',
                  {'available_loads': available_loads, 'accepted_loads': accepted_loads})


def accept_load(request, pk):
    load = Load.objects.get(pk=pk)
    carrier = Carrier.objects.get(user=request.user.pk)
    load.carrier = carrier
    load.save()
    return redirect('load:carrier-loads')


def drop_load(request, pk):
    load = Load.objects.get(pk=pk)
    carrier = Carrier.objects.get(user=request.user.pk)
    load.dropped_by.add(carrier)
    return redirect('load:carrier-loads')


