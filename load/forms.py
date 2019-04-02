from django import forms
from .models import Load

class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city', 'destination_city', 'price',)

