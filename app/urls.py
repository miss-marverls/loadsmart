from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('docs/api/', views.docs_api, name='docs_api'),
    path('docs/project/', include('docs.urls')),

]
