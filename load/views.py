from django.shortcuts import render, redirect
from .form import LoadForm
from .models import Load
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.

def register_load(request):
    return render(request, 'load/register_load.html')

def new_load(request):
    form = LoadForm(request.POST)
    if form.is_valid():
        load = form.save(commit=False)
        load.carrier = None
        load.shipper = User.objects.get(id=2)
        load.save()
        return redirect('loads')
    return render(request, 'load/new_load.html', {'form' : form})

def list_loads(request):
    available_loads = Load.objects.filter(carrier=None)
    accepted_loads = Load.objects.exclude(carrier=None)
    return render(request, 'load/list_load.html', {'available_loads' : available_loads, 'accepted_loads' : accepted_loads})

