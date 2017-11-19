from django import forms


class GetPerformanceForm(forms.Form):
    date_from = forms.DateField(required=False,
                                label="Date From",
                                input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    date_to = forms.DateField(required=False,
                              label="Date To",
                              input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField(required=False)
    price_from = forms.FloatField(required=False)
    price_to = forms.FloatField(required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
