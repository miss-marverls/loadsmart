from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html')


def docs_api(request):
    return render(request, 'app/api-doc.html')
