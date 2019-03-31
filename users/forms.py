from django.contrib.auth.forms import UserCreationForm

from . models import Shipper


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Shipper
        fields = ['first_name', 'last_name', 'email']