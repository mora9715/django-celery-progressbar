from .models import TaskProgress
from . import exceptions
from .app_settings import conf


class ProgressBar:
    """Progressbar manager class"""
    exceptions = exceptions

    def __init__(
            self,
            task_id,
            total=conf.PROGRESSBAR_DEFAULT_TOTAL,
            step=None,
            _getter=False):
        """
        :param task_id: unique task identifier
        :param total:   maximum progressbar vallue
        :param step:    verbose step name. I.e. 'finding symbolic links'
        :param _getter: internal flag
        """
        self._getter = _getter
        if self._getter:
            try:
                self._db_obj = TaskProgress.objects.get(
                    task_id=task_id
                )
            except TaskProgress.DoesNotExist:
                raise self.exceptions.DoesNotExist(task_id)
        else:
            self._db_obj = TaskProgress(
                task_id=task_id,
                total=total,
                step=step
            )
            self._db_obj.save()

    def __str__(self):
        if conf.PROGRESSBAR_DYNAMIC_UPDATE:
            self._update_db_obj()
        repr = f"{self._db_obj.progress} / {self._db_obj.total}"
        if self._db_obj.step:
            repr += f" | {self._db_obj.step}"
        return repr

    def __del__(self):
        """delete progressbar model object if configured so"""
        if not self._getter and conf.PROGRESSBAR_DESTROY_ON_EXIT:
            self._db_obj.delete()

    @property
    def progress(self):
        if conf.PROGRESSBAR_DYNAMIC_UPDATE:
            self._update_db_obj()
        return self._db_obj.progress

    @progress.setter
    def progress(self, value):
        if self._db_obj.progress + value >= self._db_obj.total:
            raise self.exceptions.OutOfRange
        self._db_obj.progress += value
        self._db_obj.save()

    @property
    def step(self):
        if conf.PROGRESSBAR_DYNAMIC_UPDATE:
            self._update_db_obj()
        return self._db_obj.step

    @step.setter
    def step(self, value):
        self._db_obj.step = value
        self._db_obj.save()

    @property
    def total(self):
        if conf.PROGRESSBAR_DYNAMIC_UPDATE:
            self._update_db_obj()
        return self._db_obj.total

    @total.setter
    def total(self, value):
        self._db_obj.total = value
        self._db_obj.save()

    @property
    def as_percent(self):
        """return current progress state in percents"""
        if conf.PROGRESSBAR_DYNAMIC_UPDATE:
            self._update_db_obj()
        return f"{(self._db_obj.progress / self._db_obj.total) * 100}%"

    @classmethod
    def get(cls, task_id):
        """
        get progressbar for a task

        :param task_id: unique task identifier
        :return: ProgressBar object
        """
        return ProgressBar(task_id, _getter=True)

    def update(self, **kwargs):
        """
        update progressbar state

        :param progress: desired bar progress
        :param step: desired bar step
        """
        if kwargs.get('progress'):
            self._db_obj.progress = kwargs['progress']
        if kwargs.get('step'):
            self._db_obj.step = kwargs['step']
        self._db_obj.save()

    def _update_db_obj(self):
        """
        update DB object
        """
        self._db_obj = TaskProgress.objects.get(
            task_id=self._db_obj.task_id
        )
    def finalize(self):
        self._db_obj.progress = self._db_obj.total
        self._db_obj.step = "Complete"
        self._db_obj.save()
