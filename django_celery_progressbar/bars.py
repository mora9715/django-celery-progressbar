from .models import TaskProgress
from . import exceptions
from .app_settings import conf


class ProgressBar:
    """Progressbar manager class"""
    exceptions = exceptions

    def __init__(self, task_id, total=conf.PROGRESSBAR_DEFAULT_TOTAL, step=None, _getter=False):
        """
        :param task_id: unique task identifier
        :param total:   maximum progressbar vallue
        :param step:    verbose step name. I.e. 'finding symbolic links'
        :param _getter: internal flag
        """
        self._getter = _getter
        if self._getter:
            try:
                self._progress_obj = TaskProgress.objects.get(
                    task_id=task_id
                )
            except TaskProgress.DoesNotExist:
                raise self.exceptions.DoesNotExist(task_id)
        else:
            self._progress_obj = TaskProgress(
                task_id=task_id,
                total=total,
                step=step
            )
            self._progress_obj.save()

    def __str__(self):
        repr = f"{self._progress_obj.progress} / {self._progress_obj.total}"
        if self._progress_obj.step:
            repr += f" | {self._progress_obj.step}"
        return repr

    def __del__(self):
        """delete progressbar model object if configured so"""
        if not self._getter and conf.PROGRESSBAR_DESTROY_ON_EXIT:
            self._progress_obj.delete()

    @property
    def progress(self):
        return self._progress_obj.progress

    @progress.setter
    def progress(self, value):
        if self._progress_obj.progress + value >= self._progress_obj.total:
            raise self.exceptions.OutOfRange
        self._progress_obj.progress += value
        self._progress_obj.save()

    @property
    def step(self):
        return self._progress_obj.step

    @step.setter
    def step(self, value):
        self._progress_obj.step = value
        self._progress_obj.save()

    @property
    def total(self):
        return self._progress_obj.total

    @total.setter
    def total(self, value):
        self._progress_obj.total = value
        self._progress_obj.save()

    @property
    def as_percent(self):
        """return current progress state in percents"""
        return f"{(self._progress_obj.progress / self._progress_obj.total) * 100}%"

    @classmethod
    def get(cls, task_id):
        """
        get progressbar for a task

        :param task_id: unique task identifier
        :return: ProgressBar object
        """
        return ProgressBar(task_id, _getter=True)

    def finalize(self):
        self._progress_obj.progress = self._progress_obj.total
        self._progress_obj.step = "Complete"