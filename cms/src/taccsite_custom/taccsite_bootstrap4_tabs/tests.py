from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Bootstrap4TabItemModel

User = get_user_model()

class Bootstrap4TabItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )

    def test_model_without_image(self):
        """We can create a Bootstrap4TabItemModel without an image"""
        tab_item = Bootstrap4TabItemModel.objects.create(
            tab_title='Test Tab Without Image'
        )

        self.assertEqual(tab_item.tab_title, 'Test Tab Without Image')
        self.assertIsNone(tab_item.tab_image)

    def test_model_has_tab_image_field(self):
        """The model has the tab_image field defined"""
        tab_item = Bootstrap4TabItemModel()
        self.assertTrue(hasattr(tab_item, 'tab_image'))

        # The field is a `FilerImageField`
        field = Bootstrap4TabItemModel._meta.get_field('tab_image')
        self.assertEqual(field.verbose_name, 'Tab Image/Thumbnail')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_extend_function_exists(self):
        """The extend function can be imported and called"""
        from .extend import extendBootstrap4TabsPlugin

        # Extending plugin raises no exceptions
        extendBootstrap4TabsPlugin()
