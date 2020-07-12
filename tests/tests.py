import pytest
from django.test import TestCase

from django_celery_progressbar.bars import ProgressBar
from django_celery_progressbar.models import TaskProgress


class BarTestCase(TestCase):
    def setUp(self):
        TaskProgress.objects.create(
            task_id='xxx-yyy-zzz',
            step='Brewing coffee',
            total=100
        )

    def test_finalize(self):
        bar = ProgressBar.get('xxx-yyy-zzz')
        bar.finalize()
        assert bar.total == bar.progress, 'progress should be the same as total'

    def test_dynamic_updates(self):
        bar = ProgressBar('xxx-yyy-zzz', _getter=True, dynamic=True)
        task = TaskProgress.objects.get(task_id='xxx-yyy-zzz')
        task.progress = 66
        task.save()

        assert bar.progress == task.progress, 'dynamic update does not work'


class ExceptionTestCase(TestCase):
    def setUp(self):
        TaskProgress.objects.create(
            task_id='xxx-yyy-zzz',
            step='Brewing coffee',
            total=100
        )

    def test_does_not_exist(self):
        with pytest.raises(ProgressBar.exceptions.DoesNotExist):
            ProgressBar.get('asd')

    def test_out_of_range(self):
        with pytest.raises(ProgressBar.exceptions.OutOfRange):
            bar = ProgressBar.get('xxx-yyy-zzz')
            bar.progress += 200

        with pytest.raises(ProgressBar.exceptions.OutOfRange):
            bar = ProgressBar.get('xxx-yyy-zzz')
            bar.update(
                progress=200
            )
