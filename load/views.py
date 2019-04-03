from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LoadForm
from .models import Load
from users.models import Shipper
from bootstrap_modal_forms.generic import BSModalCreateView


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
        return redirect('load:loads')


def list_loads(request):
    available_loads = Load.objects.filter(carrier=None)
    accepted_loads = Load.objects.exclude(carrier=None)
    return render(request, 'load/list_load.html', {'available_loads' : available_loads, 'accepted_loads' : accepted_loads})

