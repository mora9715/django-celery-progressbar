=================
Usage
=================

Some examples of typical package usages can be found below.

Inside Celery task:

.. code-block:: python

    from django_celery_progressbar.bars import ProgressBar
    from celery import shared_task

    @shared_task
    def do_something():
        bar = ProgressBar(
            task_id=do_something.request.id,
            total=10,
            step='Drying kelp...'
        )

        some_work()
        bar.update(
            progress='5',
            step='Making sushi...'
        )

        some_more_work()
        bar.progress.finalize()

To retireve current progressbar state, use a built-in getter:

.. code-block:: python

    from django_celery_progressbar.bars import ProgressBar

    bar = ProgressBar.get(task_id)
    print(bar)

    >>> 5 / 10 | Drying kelp...

    # or as percent:
    print(bar.as_percent)

    >>> 50.0%

Keep in mind: ProgressBar fetches model object on creation, it is not updated dynamically.

To enable dynamic updates, see :ref:`PROGRESSBAR_DYNAMIC_UPDATE <progressbar_dynamic_update>`