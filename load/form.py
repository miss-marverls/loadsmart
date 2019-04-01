from django import forms
#from bootstrap_modal_forms.forms import BSModalForm
from .models import Load

#class LoadForm(forms.ModelForm):
class LoadForm(forms.ModelForm):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city', 'destination_city', 'price',)

