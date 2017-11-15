from django.test import TestCase
from .services import *
from .forms import AddPerformanceForm
from django.http import HttpRequest


class AddPerformanceFormTest(TestCase):
    def setUp(self):
        pass

    def test_form_is_valid(self):
        payload = {'date': '01-01-2030',
                   'time': '10:10',
                   'price': 100,
                   'description': 'bla',
                   'features': ['cat', 'dog', 'human'],
                   'ticketsNumber': 10}
        f = AddPerformanceForm(payload)
        f.is_valid()
        self.assertEqual(f.cleaned_data['features'][0], 'cat')

