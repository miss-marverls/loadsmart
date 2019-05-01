from bootstrap_modal_forms.forms import BSModalForm
from django import forms

from .models import Load


class DateInput(forms.DateInput):
    """
    Form used for pickup date input.
    """

    input_type = 'date'


class LoadForm(BSModalForm):
    """
    Popup form used for load creation.
    """

    class Meta:
        model = Load
        fields = ('pickup_date', 'ref', 'origin_city',
                  'destination_city', 'shipper_price',)
        widgets = {
            'pickup_date': DateInput(),
        }


class LoadEditRateForm(BSModalForm):
    """
    Popup form used for load rate edition.

    The shipper can edit the load price suggested by the data science model.
    """

    class Meta:
        model = Load
        fields = ('shipper_price',)
