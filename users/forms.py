from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from . models import User

class ShipperCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CarrierCreationForm(UserCreationForm):
    mc_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mc_number']
