from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .form import LoadForm
from .models import Load
from users.models import Shipper
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

# Create your views here.

class LoadCreateView(BSModalCreateView):
    template_name = 'load/new_load.html'
    form_class = Load
    success_message = 'Success: Load was registered.'
    success_url = reverse_lazy('loads')


def register_load(request):
    return render(request, 'load/register_load.html')

def new_load(request):
    form = LoadForm(request.POST)
    if form.is_valid():
        load = form.save(commit=False)
        load.carrier = None
        if request.user.is_authenticated:
            load.shipper = request.user
        load.save()
        return redirect('loads')
    return render(request, 'load/new_load.html', {'form' : form})

def list_loads(request):
    available_loads = Load.objects.filter(carrier=None)
    accepted_loads = Load.objects.exclude(carrier=None)
    return render(request, 'load/list_load.html', {'available_loads' : available_loads, 'accepted_loads' : accepted_loads})

