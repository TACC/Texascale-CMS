from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Bootstrap4TabItem, TabImageExtension

User = get_user_model()

class Bootstrap4TabItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )

    def test_model_without_image(self):
        """We can create a Bootstrap4TabItem without an image"""
        tab_item = Bootstrap4TabItem.objects.create(
            tab_title='Test Tab Without Image'
        )

        self.assertEqual(tab_item.tab_title, 'Test Tab Without Image')
        self.assertIsNone(tab_item.tab_image)

    def test_model_has_tab_image_field(self):
        """The image field is defined on the extension model"""
        field = TabImageExtension._meta.get_field('tab_image')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
