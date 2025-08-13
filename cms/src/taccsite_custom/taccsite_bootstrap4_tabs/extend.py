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

    from .models import Bootstrap4TabItem, TabImageExtension

    class Bootstrap4TabItemForm(forms.ModelForm):
        tab_image = forms.ImageField(
            label=_('Tab Image/Thumbnail'),
            required=False,
        )

        class Meta:
            model = Bootstrap4TabItem
            fields = ('tab_title',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                try:
                    extension = getattr(self.instance, 'image_extension', None)
                    if extension:
                        self.fields['tab_image'].initial = extension.tab_image
                except TabImageExtension.DoesNotExist:
                    # This is a legacy tab item created before the extension
                    pass

        def save(self, commit=True):
            instance = super().save(commit=False)
            if commit:
                instance.save()
                if 'tab_image' in self.cleaned_data and self.cleaned_data['tab_image']:
                    extension, _ = TabImageExtension.objects.get_or_create(
                        bootstrap4_tab_item=instance
                    )
                    extension.tab_image = self.cleaned_data['tab_image']
                    extension.save()
            return instance

    class Bootstrap4TabItemPlugin(OriginalBootstrap4TabItemPlugin):
        model = Bootstrap4TabItem
        form = Bootstrap4TabItemForm
        name = "Tab Item (supports Image)"

        fieldsets = [
            (None, {
                'fields': (
                    'tab_title',
                )
            }),
            (_('Image'), {
                'fields': (
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
                'tab_image': instance.tab_image,
            })
            return context

    plugin_pool.unregister_plugin(OriginalBootstrap4TabItemPlugin)
    plugin_pool.register_plugin(Bootstrap4TabItemPlugin)
