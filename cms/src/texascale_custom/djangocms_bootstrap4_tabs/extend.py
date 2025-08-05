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
    from djangocms_bootstrap4.contrib.bootstrap4_tabs.models import (
        Bootstrap4TabItem as OriginalBootstrap4TabItem
    )

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
                        f"Please select a valid image or remove the image reference. "
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

    class Bootstrap4TabItemForm(forms.ModelForm):
        tab_image = forms.ModelChoiceField(
            queryset=Image.objects.all(),
            required=False,
            label=_('Tab Image/Thumbnail'),
            help_text=_('Optional image to display in the tab title for slideshow navigation'),
            widget=forms.Select(attrs={
                'class': 'filer-image-select',
                'data-placeholder': _('Select an image...')
            })
        )

        class Meta:
            model = OriginalBootstrap4TabItem
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if self.instance and self.instance.pk:
                if hasattr(self.instance, 'attributes') and self.instance.attributes:
                    image_id = self.instance.attributes.get('data-tab-image-id')
                    if image_id:
                        try:
                            image = Image.objects.get(id=image_id)
                            self.fields['tab_image'].initial = image
                            self.initial['tab_image'] = image
                        except (Image.DoesNotExist, ValueError, TypeError):
                            # Clean up invalid reference
                            if hasattr(self.instance, 'attributes') and 'data-tab-image-id' in self.instance.attributes:
                                del self.instance.attributes['data-tab-image-id']

        def clean(self):
            cleaned_data = super().clean()

            if hasattr(self.instance, '__dict__'):
                self.instance._form_data = cleaned_data

            return cleaned_data

        def save(self, commit=True):
            instance = super().save(commit=False)

            tab_image = self.cleaned_data.get('tab_image')
            if not hasattr(instance, 'attributes') or instance.attributes is None:
                instance.attributes = {}

            if tab_image:
                instance.attributes['data-tab-image-id'] = str(tab_image.id)
            elif 'data-tab-image-id' in instance.attributes:
                del instance.attributes['data-tab-image-id']

            if commit:
                instance.save()
            return instance

    class Bootstrap4TabItemModel(OriginalBootstrap4TabItem):
        class Meta:
            proxy = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not hasattr(self, 'attributes') or self.attributes is None:
                self.attributes = {}

        def clean(self):
            cleaned_data = super().clean()
            validate_tab_image(self)
            return cleaned_data

        @property
        def tab_image(self):
            """Get the tab image from attributes"""
            if not hasattr(self, '_tab_image_cache'):
                self._tab_image_cache = None
                if hasattr(self, 'attributes') and self.attributes:
                    image_id = self.attributes.get('data-tab-image-id')
                    if image_id:
                        try:
                            self._tab_image_cache = Image.objects.get(id=image_id)
                        except (Image.DoesNotExist, ValueError, TypeError):
                            pass
            return self._tab_image_cache

        @tab_image.setter
        def tab_image(self, value):
            """Set the tab image in attributes"""
            self._tab_image_cache = value
            if not hasattr(self, 'attributes') or self.attributes is None:
                self.attributes = {}

            if value:
                self.attributes['data-tab-image-id'] = str(value.id)
            elif 'data-tab-image-id' in self.attributes:
                del self.attributes['data-tab-image-id']

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

            tab_image = None
            if instance.attributes and 'data-tab-image-id' in instance.attributes:
                try:
                    tab_image = Image.objects.get(id=instance.attributes['data-tab-image-id'])
                except (Image.DoesNotExist, ValueError, TypeError):
                    # Clean up invalid reference
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
