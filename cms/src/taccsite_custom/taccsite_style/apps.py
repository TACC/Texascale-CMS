from django.apps import AppConfig

from .extend import extendStylePlugin

class TaccsiteStyleConfig(AppConfig):
    name = 'taccsite_custom.taccsite_style'
    label = 'taccsite_style'
    verbose_name = 'TACC Style'

    def ready(self):
        extendStylePlugin()
