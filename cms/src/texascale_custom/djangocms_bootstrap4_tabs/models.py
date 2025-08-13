from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

from djangocms_bootstrap4.contrib.bootstrap4_tabs.models import (
    Bootstrap4TabItem as OriginalBootstrap4TabItem
)


class TabImageExtension(models.Model):
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

class Bootstrap4TabItem(OriginalBootstrap4TabItem):
    class Meta:
        proxy = True

    def copy_relations(self, old_instance):
        super().copy_relations(old_instance)
        if hasattr(old_instance, 'image_extension'):
            # new_extension is not used, but this creates the object
            new_extension = TabImageExtension.objects.create(
                bootstrap4_tab_item=self,
                tab_image=old_instance.image_extension.tab_image
            )

    @property
    def tab_image(self):
        if hasattr(self, 'image_extension'):
            return self.image_extension.tab_image
        return None
