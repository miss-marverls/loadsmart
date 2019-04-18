from django import forms
from .models import Load
from bootstrap_modal_forms.forms import BSModalForm


class DateInput(forms.DateInput):
    input_type = 'date'


class LoadForm(BSModalForm):
    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city',
                  'destination_city', 'shipper_price',)
        widgets = {
            'pickup_date': DateInput(),
        }


class LoadEditRateForm(BSModalForm):
    class Meta:
        model = Load
        fields = ('shipper_price',)
