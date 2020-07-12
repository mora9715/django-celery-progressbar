class OutOfRange(Exception):
    """Raised when resulting *progress* is more than *total* value."""
    def __init__(self):
        super(OutOfRange, self).__init__(
            "resulting progress is out of range"
        )


class DoesNotExist(Exception):
    """Raised when requested Celery task does not exist.

    :param: task_id: Unique task identifier.
    :type task_id: str.
    """
    def __init__(self, task_id):
        super(DoesNotExist, self).__init__(
            f"requested progressbar for task {task_id} does not exist"
        )
