from django.shortcuts import render
# Create your views here.

def register_load(request):
    return render(request, 'load/register_load.html')

