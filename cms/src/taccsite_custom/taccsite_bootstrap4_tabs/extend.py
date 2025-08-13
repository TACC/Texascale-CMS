import logging

logger = logging.getLogger(f"portal.{__name__}")

def extendBootstrap4TabsPlugin():
    from django import forms
    from django.utils.translation import gettext_lazy as _
    from django.contrib import admin

    from cms.plugin_pool import plugin_pool

    # djangocms_bootstrap4
    from djangocms_bootstrap4.contrib.bootstrap4_tabs.cms_plugins import (
        Bootstrap4TabItemPlugin as OriginalBootstrap4TabItemPlugin
    )

    from .models import Bootstrap4TabItem, TabImageExtension

    class TabImageExtensionInline(admin.TabularInline):
        """
        Inline admin for TabImageExtension that appears within the main plugin form.
        This gives us the proper Filer image picker without fieldset validation issues.
        """
        model = TabImageExtension

        verbose_name = _("Image list")
        verbose_name_plural = _("Images list")

        extra = 1 # Show one by default
        # max_num = 1 # Already explicitly limited by model's OneToOneField
        can_delete = False # Don't allow deletion of the extension

        # Use all fields from the extension model
        fields = ('tab_image',)

    class Bootstrap4TabItemPlugin(OriginalBootstrap4TabItemPlugin):
        model = Bootstrap4TabItem
        name = "Tab Item (with Image support)"

        inlines = [TabImageExtensionInline]

        fieldsets = [
            (None, {
                'fields': (
                    'tab_title',
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
