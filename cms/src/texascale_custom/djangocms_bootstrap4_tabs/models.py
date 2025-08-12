from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

# djangocms_bootstrap4
from djangocms_bootstrap4.contrib.bootstrap4_tabs.models import (
    Bootstrap4TabItem as OriginalBootstrap4TabItem
)


class Bootstrap4TabItemModel(OriginalBootstrap4TabItem):
    tab_image = FilerImageField(
        verbose_name=_('Tab Image/Thumbnail'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Optional image to display in the tab title for slideshow navigation')
    )

    class Meta:
        proxy = False  # CRITICAL: Change from True to False