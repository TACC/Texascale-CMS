from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

from djangocms_bootstrap4.contrib.bootstrap4_tabs.models import (
    Bootstrap4TabItem as OriginalBootstrap4TabItem
)


class TabImageExtension(models.Model):
    class Meta:
        app_label = 'taccsite_bootstrap4_tabs'

    bootstrap4_tab_item = models.OneToOneField(
        OriginalBootstrap4TabItem,
        on_delete=models.CASCADE,
        related_name="image_extension",
        primary_key=True,
    )
    tab_image = FilerImageField(
        verbose_name=_('Tab Image/Thumbnail'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Optional image to display in the tab title for slideshow navigation')
    )

    def __str__(self):
        if self.tab_image:
            return f"Tab image: {self.tab_image.name}"
        return "Tab image (no image)"

class Bootstrap4TabItem(OriginalBootstrap4TabItem):
    class Meta:
        proxy = True

    def copy_relations(self, old_instance):
        super().copy_relations(old_instance)
        if hasattr(old_instance, 'image_extension'):
            # This `new_extension` is not used, but it creates the object
            new_extension = TabImageExtension.objects.create(
                bootstrap4_tab_item=self,
                tab_image=old_instance.image_extension.tab_image
            )

    @property
    def tab_image(self):
        """
        Get the tab image for this tab item.
        
        Returns None for:
        - Legacy tabs (created before extension)
        - New tabs where no image was uploaded
        """
        image_extension = getattr(self, 'image_extension', None)
        if image_extension:
            return image_extension.tab_image
        return None
