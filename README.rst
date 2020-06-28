====================================
Django Celery Progressbar
====================================

.. image:: https://travis-ci.org/mora9715/django-celery-progressbar.svg?branch=master
  :target: https://travis-ci.org/mora9715/django-celery-progressbar

.. image:: https://badge.fury.io/py/django-celery-progressbar.svg
  :target: https://badge.fury.io/py/django-celery-progressbar

Simple progressbar for a Django application with Celery. Uses database as a temporary storage.

============
Installation
============

Installation is as simple as installing a package from PyPi and applying migrations::

    $ pip install django-celery-progresbar
    $ python manage.py migrate django_celery_progressbar

=================
Usage
=================

Typical usage on the side of Celery task would look like:

.. code-block:: python

    from django_celery_progressbar.bars import ProgressBar
    from celery import shared_task

    @shared_task
    def do_something():
        bar = ProgressBar(
            task_id=do_something.request.id,
            total=10,
            step= 'Drying kelp...'
        )

        some_work()
        bar.progress += 5
        bar.step = 'Making sushi...'

        some_more_work()
        bar.progress.finalize()

To retireve current progressbar state, you can use built-in getter:

.. code-block:: python

    from django_celery_progressbar.bars import ProgressBar

    bar = ProgressBar.get(task_id)
    print(bar)

    >>> 5 / 10 | Drying kelp...

    # or as percent:
    print(bar.as_percent)

    >>> 50%

=================
Configuration
=================

The following default settings can be overridden in your *settings.py*:

.. code-block:: python

    PROGRESSBAR_DEFAULT_TOTAL = 100
    PROGRESSBAR_DESTROY_ON_EXIT = False


**PROGRESSBAR_DEFAULT_TOTAL** - Default value for 'Total' progressbar attribute
**PROGRESSBAR_DESTROY_ON_EXIT** - Destroy model object on task completion

=======
License
=======

* Free software: MIT license
