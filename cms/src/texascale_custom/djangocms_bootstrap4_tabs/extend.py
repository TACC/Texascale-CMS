import logging

logger = logging.getLogger(f"portal.{__name__}")

def extendBootstrap4TabsPlugin():
    from django import forms
    from django.utils.translation import gettext_lazy as _

    from cms.plugin_pool import plugin_pool

    from filer.models import Image

    # djangocms_bootstrap4
    from djangocms_bootstrap4.contrib.bootstrap4_tabs.cms_plugins import (
        Bootstrap4TabItemPlugin as OriginalBootstrap4TabItemPlugin
    )
    
    # Import our custom model
    from .models import Bootstrap4TabItemModel

    class Bootstrap4TabItemForm(forms.ModelForm):
        class Meta:
            model = Bootstrap4TabItemModel
            fields = '__all__'
            # FilerImageField automatically provides the correct widget!

    class Bootstrap4TabItemPlugin(OriginalBootstrap4TabItemPlugin):
        model = Bootstrap4TabItemModel
        form = Bootstrap4TabItemForm
        name = "Tab Item (supports Image)"

        fieldsets = [
            (None, {
                'fields': (
                    'tab_title',
                    'tab_image',
                )
            }),
            (_('Advanced settings'), {
                'classes': ('collapse',),
                'fields': (
                    'tag_type',
                    'attributes',
                )
            }),
        ]

        def render(self, context, instance, placeholder):
            context = super().render(context, instance, placeholder)
            is_old_plugin_instance = not hasattr(instance, 'tab_image')

            if is_old_plugin_instance:
                tab_image = None
            else:
                tab_image = instance.tab_image

            context.update({
                'tab_image': tab_image,
            })

            return context

    try:
        plugin_pool.unregister_plugin(OriginalBootstrap4TabItemPlugin)
    except Exception as e:
        logger.warning(f"Could not unregister original plugin: {e}")
    
    plugin_pool.register_plugin(Bootstrap4TabItemPlugin)