class OutOfRange(Exception):
    def __init__(self):
        super(OutOfRange, self).__init__(
            "resulting progress is out of range"
        )


class DoesNotExist(Exception):
    def __init__(self, task_id):
        super(DoesNotExist, self).__init__(
            f"requested progressbar for task {task_id} does not exist"
        )
