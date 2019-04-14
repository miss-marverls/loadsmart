from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import Shipper


class ShipperCreationForm(UserCreationForm):

    class Meta:
        model = Shipper
        fields = ['first_name', 'last_name', 'email']


class CarrierCreationForm(UserCreationForm):
    mc_number = forms.CharField(required=True)
    class Meta:
        model = Shipper
        fields = [ 'first_name', 'last_name', 'email','mc_number']
