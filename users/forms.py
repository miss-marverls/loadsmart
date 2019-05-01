from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class ShipperCreationForm(UserCreationForm):
    """Form for Shipper creation."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CarrierCreationForm(UserCreationForm):
    """Form for Carrier creation."""

    mc_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mc_number']
