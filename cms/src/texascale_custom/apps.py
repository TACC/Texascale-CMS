from django.apps import AppConfig

class TexascaleCustomConfig(AppConfig):
    name = 'texascale_custom'
    label = 'texascale_custom'
    verbose_name = 'TACC CMS (Texascale Customizations)'

    def ready(self):
        from .djangocms_bootstrap4_tabs.extend import extendBootstrap4TabsPlugin

        extendBootstrap4TabsPlugin()
