from . import exceptions
from .app_settings import conf
from .models import TaskProgress


class ProgressBar:
    """Base progressbar class.

    :param task_id: Unique task identifier.
    :type task_id: str.
    :param total:   Maximum progressbar value.
    :type total: int.
    :param step:    Verbose step name. I.e. 'finding symbolic links'
    :type step: str.
    :param dynamic: Enable dynamic updates.
    :type dynamic: bool.

    :raises: ProgressBar.exceptions.OutOfRange, ProgressBar.exceptions.DoesNotExist
    """
    exceptions = exceptions

    def __init__(
            self,
            task_id,
            total=conf.PROGRESSBAR_DEFAULT_TOTAL,
            step=None,
            dynamic=conf.PROGRESSBAR_DYNAMIC_UPDATE,
            _getter=False):

        self.dynamic = dynamic
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
        if self.dynamic:
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
        """Return current bar progress.

        :returns:  int -- current progress.
        """
        if self.dynamic:
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
        """Return current bar step.

        :returns:  str -- current step.
        """
        if self.dynamic:
            self._update_db_obj()
        return self._db_obj.step

    @step.setter
    def step(self, value):
        self._db_obj.step = value
        self._db_obj.save()

    @property
    def total(self):
        """Return total bar value.

        :returns: int -- total value.
        """
        if self.dynamic:
            self._update_db_obj()
        return self._db_obj.total

    @total.setter
    def total(self, value):
        self._db_obj.total = value
        self._db_obj.save()

    @property
    def as_percent(self):
        """Return current progress state in percents.

        :returns: str -- current progress in percents.
        """
        if self.dynamic:
            self._update_db_obj()
        return f"{(self._db_obj.progress / self._db_obj.total) * 100}%"

    @classmethod
    def get(cls, task_id):
        """Get progressbar for a task.

        :param task_id: Unique task identifier.
        :type task_id: str.

        :returns: ProgressBar object
        """
        return ProgressBar(task_id, _getter=True)

    def update(self, **kwargs):
        """Update progressbar state.

        :param progress: Desired bar progress.
        :type progress: int.
        :param step: Desired bar step.
        :type step: str.

        :return: None
        """
        if kwargs.get('progress'):
            if self._db_obj.progress + kwargs.get('progress') >= self._db_obj.total:
                raise self.exceptions.OutOfRange
            self._db_obj.progress = kwargs['progress']
        if kwargs.get('step'):
            self._db_obj.step = kwargs['step']
        self._db_obj.save()

    def _update_db_obj(self):
        """Update related database object.

        :return: None
        """
        self._db_obj = TaskProgress.objects.get(
            task_id=self._db_obj.task_id
        )

    def finalize(self):
        """Finalize progressbar, setting *progress* equal to *total* and *Complete* step.

        :return: None
        """
        self._db_obj.progress = self._db_obj.total
        self._db_obj.step = "Complete"
        self._db_obj.save()
