import logging

logger = logging.getLogger(f"portal.{__name__}")

def extendBootstrap4TabsPlugin():
    from django import forms
    from django.utils.translation import gettext_lazy as _

    from cms.plugin_pool import plugin_pool

    from filer.models import Image

    def validate_tab_image(instance):
        """Validates that the tab image exists and is valid"""
        from django.core.exceptions import ValidationError

        errors = {}

        if hasattr(instance, 'attributes') and instance.attributes:
            image_id = instance.attributes.get('data-tab-image-id')
            if image_id:
                try:
                    Image.objects.get(id=image_id)
                except Image.DoesNotExist:
                    errors['tab_image'] = _(
                        f"Selected image (ID: {image_id}) no longer exists in the file manager. "
                        "Please select a new image or remove the image reference."
                    )
                except (ValueError, TypeError) as e:
                    errors['tab_image'] = _(
                        f"Please select a valid image or remove the image reference."
                        f"ERROR: {str(e)}"
                    )

        if errors:
            raise ValidationError(errors)

    def filter_attributes_str(attributes):
        """
        Create HTML attributes string excluding internal data.
        """
        if not attributes:
            return ""

        filtered_attributes = {
            k: v for k, v in attributes.items()
            if k not in ['data-tab-image-id']
        }

        if not filtered_attributes:
            return ""

        attr_parts = []
        for key, value in filtered_attributes.items():
            if value is not None and value != '':
                attr_parts.append(f'{key}="{value}"')

        return ' ' + ' '.join(attr_parts) if attr_parts else ""


    # djangocms_bootstrap4
    from djangocms_bootstrap4.contrib.bootstrap4_tabs.cms_plugins import (
        Bootstrap4TabItemPlugin as OriginalBootstrap4TabItemPlugin
    )
    from djangocms_bootstrap4.contrib.bootstrap4_tabs.models import (
        Bootstrap4TabItem as OriginalBootstrap4TabItem
    )

    class Bootstrap4TabItemForm(OriginalBootstrap4TabItemPlugin.form):
        tab_image = forms.ModelChoiceField(
            queryset=Image.objects.all(),
            required=False,
            label=_('Tab Image/Thumbnail'),
            help_text=_('Optional image to display in the tab title for slideshow navigation')
        )

    class Bootstrap4TabItemModel(OriginalBootstrap4TabItem):
        class Meta:
            proxy = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not hasattr(self, 'attributes') or self.attributes is None:
                self.attributes = {}

        def _initialize_tab_image(self):
            """Initialize the tab_image property from attributes"""
            if hasattr(self, 'attributes') and self.attributes:
                image_id = self.attributes.get('data-tab-image-id')
                if image_id:
                    self.tab_image = Image.objects.filter(id=image_id).first()

        def clean(self):
            cleaned_data = super().clean()

            form_data = getattr(self, '_form_data', {})
            if 'tab_image' in form_data:
                tab_image = form_data['tab_image']
                if tab_image:
                    self.attributes['data-tab-image-id'] = str(tab_image.id)
                elif 'data-tab-image-id' in self.attributes:
                    logger.debug(
                        "Cleaning up orphaned tab image reference: %s",
                        self.attributes['data-tab-image-id']
                    )
                    del self.attributes['data-tab-image-id']

            validate_tab_image(self)

            if not hasattr(self, '_tab_image_initial_set'):
                self._initialize_tab_image()
                self._tab_image_initial_set = True

            return cleaned_data

        @property
        def tab_image(self):
            if not hasattr(self, '_tab_image'):
                self._tab_image = None
                image_id = self.attributes.get('data-tab-image-id')
                if image_id:
                    try:
                        self._tab_image = Image.objects.get(id=image_id)
                    except (Image.DoesNotExist, ValueError):
                        pass
            return self._tab_image

        @tab_image.setter
        def tab_image(self, value):
            self._tab_image = value
            if value:
                self.attributes['data-tab-image-id'] = str(value.id)
            elif 'data-tab-image-id' in self.attributes:
                del self.attributes['data-tab-image-id']

    class Bootstrap4TabItemPlugin(OriginalBootstrap4TabItemPlugin):
        model = Bootstrap4TabItemModel
        form = Bootstrap4TabItemForm
        
        # Add the tab_image field to the fieldsets
        fieldsets = [
            (None, {
                'fields': (
                    'tab_title',
                    'tag_type',
                    'tab_image',
                )
            }),
            (None, {
                'fields': (
                    'attributes',
                )
            })
        ]

        def get_form(self, request, obj=None, **kwargs):
            form = super().get_form(request, obj, **kwargs)
            return form

        def render(self, context, instance, placeholder):
            context = super().render(context, instance, placeholder)

            tab_image = None
            if instance.attributes and 'data-tab-image-id' in instance.attributes:
                try:
                    tab_image = Image.objects.get(id=instance.attributes['data-tab-image-id'])
                except (Image.DoesNotExist, ValueError):
                    del instance.attributes['data-tab-image-id']
                    instance.save()

            context.update({
                'tab_image': tab_image,
                'has_tab_image': tab_image is not None,
                'filtered_attributes_str': filter_attributes_str(instance.attributes or {})
            })

            return context

    plugin_pool.unregister_plugin(OriginalBootstrap4TabItemPlugin)
    plugin_pool.register_plugin(Bootstrap4TabItemPlugin)
