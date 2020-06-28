from django.conf import settings

PROGRESSBAR_DEFAULTS = {
    'PROGRESSBAR_DEFAULT_TOTAL': 100,
    'PROGRESSBAR_DESTROY_ON_EXIT': False
}


class AppSettings:
    """Allowing to override module settings from django config"""

    def __init__(self, defaults):
        for key in defaults:
            if getattr(settings, key, None):
                setattr(self, key, getattr(settings, key))
            else:
                setattr(self, key, defaults[key])


conf = AppSettings(PROGRESSBAR_DEFAULTS)
