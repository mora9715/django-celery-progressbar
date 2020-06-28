from pkg_resources import DistributionNotFound, get_distribution

__author__ = 'Eugene Prodan'
__email__ = 'mora9715@gmail.com'

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

default_app_config = 'django_celery_progressbar.apps.ProgressBarConfig'
