from django.shortcuts import render, redirect


def index(request):
    return redirect('users:login')


def docs_api(request):
    return render(request, 'app/api-doc.html')
