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

    def filter_attributes_str(attributes):
        """
        Create HTML attributes string from attributes dict.
        """
        if not attributes:
            return ""

        attr_parts = []
        for key, value in attributes.items():
            if value is not None and value != '':
                attr_parts.append(f'{key}="{value}"')

        return ' ' + ' '.join(attr_parts) if attr_parts else ""

    class Bootstrap4TabItemForm(forms.ModelForm):
        class Meta:
            model = Bootstrap4TabItemModel
            fields = '__all__'
            # FilerImageField automatically provides the correct widget!

    class Bootstrap4TabItemPlugin(OriginalBootstrap4TabItemPlugin):
        model = Bootstrap4TabItemModel
        form = Bootstrap4TabItemForm

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

            context.update({
                'tab_image': instance.tab_image,  # Direct field access!
                'has_tab_image': bool(instance.tab_image),
                'filtered_attributes_str': filter_attributes_str(instance.attributes or {})
            })

            return context

    plugin_pool.unregister_plugin(OriginalBootstrap4TabItemPlugin)
    plugin_pool.register_plugin(Bootstrap4TabItemPlugin)
