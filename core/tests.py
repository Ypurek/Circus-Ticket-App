from django.test import TestCase
from core.models import Ticket, Performance, Feature
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
