from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User


class ShipperCreationForm(UserCreationForm):
    """
    Form for Shipper creation.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CarrierCreationForm(UserCreationForm):
    """
    Form for Carrier creation.

    Validates MC number format according to FMCSA website
    """

    re_mc_number = RegexValidator(
        '^[a-zA-Z]{2}[0-9]{6}$', 'MC number must be prefixed by 2 letters and followed by 6 numbers')
    mc_number = forms.CharField(required=True, validators=[re_mc_number])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mc_number']
