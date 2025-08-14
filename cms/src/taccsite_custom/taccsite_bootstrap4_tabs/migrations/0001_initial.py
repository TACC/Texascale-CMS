from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bootstrap4_tabs', '0002_auto_20180610_1106'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bootstrap4TabItem',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bootstrap4_tabs.bootstrap4tabitem',),
        ),
        migrations.CreateModel(
            name='TabImageExtension',
            fields=[
                ('bootstrap4_tab_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='image_extension', serialize=False, to='bootstrap4_tabs.bootstrap4tabitem')),
                ('tab_image', filer.fields.image.FilerImageField(blank=True, help_text='Optional image to display in the tab title for slideshow navigation', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.FILER_IMAGE_MODEL, verbose_name='Image/Thumbnail')),
            ],
        ),
    ]
