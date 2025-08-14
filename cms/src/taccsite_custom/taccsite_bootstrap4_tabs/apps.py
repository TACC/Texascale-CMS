from django.apps import AppConfig

from .extend import extendBootstrap4TabsPlugin

class TaccsiteBootstrap4TabsConfig(AppConfig):
    name = 'taccsite_custom.taccsite_bootstrap4_tabs'
    label = 'taccsite_bootstrap4_tabs'
    verbose_name = 'TACC Bootstrap4 Tabs'

    def ready(self):
        extendBootstrap4TabsPlugin()
