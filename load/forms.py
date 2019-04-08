from django import forms
from .models import Load
from bootstrap_modal_forms.forms import BSModalForm


class LoadForm(BSModalForm):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city', 'destination_city', 'price',)


class LoadEditRateForm(BSModalForm):
    class Meta:
        model = Load
        fields = ('price',)
