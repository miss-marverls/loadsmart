from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import User
from django.core.validators import RegexValidator

class ShipperCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CarrierCreationForm(UserCreationForm):
    re_mc_number = RegexValidator('^[a-zA-Z]{2}[0-9]{6}$', 'MC number must be prefixed by 2 letters and followed by 6 numbers')
    mc_number = forms.CharField(required=True, validators=[re_mc_number])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mc_number']
