from django.test import TestCase
from core.models import Ticket, Performance, Feature, AppSettings
from core import processing


class TestProcessing(TestCase):
    def setUp(self):
        Feature.objects.create(feature='dog')

    def test_feature_can_be_added(self):
        result = processing.add_feature('cat')
        self.assertEqual(result[0].feature, 'cat')
        self.assertEqual(result[1], True)

    def test_feature_cannot_be_added_twice(self):
        result = processing.add_feature('dog')
        self.assertEqual(result[0].feature, 'dog')
        self.assertEqual(result[1], False)


class TestProperties(TestCase):
    def setUp(self):
        processing.set_app_property('new_property', 'value')
        processing.set_app_property('new_property2', 'value')

    def test_get_property(self):
        value = processing.get_app_property('new_property')
        self.assertEqual(value, 'value')

    def test_set_property(self):
        processing.set_app_property('new_property2', 'modified value')
        value = processing.get_app_property('new_property2')
        prop = AppSettings.objects.filter(property='new_property2')
        self.assertEqual(value, 'modified value', 'property value not updated')
        self.assertEqual(len(prop), 1, 'property duplicated')

