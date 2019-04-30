from django.shortcuts import render


def index(request):
    return render(request, 'users/login.html')


def docs(request):
    return render(request, 'app/api-doc.html')
