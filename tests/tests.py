from django.test import TestCase
import django_celery_progressbar

class AnimalTestCase(TestCase):
    def setUp(self):
        print('setup')

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        print('task')
        print(django_celery_progressbar.__file__)