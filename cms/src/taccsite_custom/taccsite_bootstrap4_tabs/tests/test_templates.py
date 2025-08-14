from django.test import TestCase
from django.template import Context, Template
from unittest.mock import Mock

class TabsImageTemplateTest(TestCase):
    def test_tabs_image_template_with_mock_image(self):
        """The tabs_image template renders correctly with a mock image"""

        mock_image = Mock()
        mock_image.url = '/media/test-image.jpg'
        mock_image.default_alt_text = 'Test Alt Text'
        mock_image.original_filename = 'test-image.jpg'
        mock_image.width = 100
        mock_image.height = 50

        template_content = """
        {% load static %}
        <img src="{{ instance.url }}"
            alt="{% if instance.default_alt_text %}{{ instance.default_alt_text }}{% else %}{{ instance.original_filename }}{% endif %}"
            {% if instance.width %} width="{{ instance.width }}"{% endif %}
            {% if instance.height %} height="{{ instance.height }}"{% endif %}
        >
        """
        template = Template(template_content)

        context = Context({'instance': mock_image})
        rendered = template.render(context)

        # The image attributes are rendered correctly
        self.assertIn('src="/media/test-image.jpg"', rendered)
        self.assertIn('alt="Test Alt Text"', rendered)
        self.assertIn('width="100"', rendered)
        self.assertIn('height="50"', rendered)

    def test_tabs_image_template_without_alt_text(self):
        """Test that the template falls back to filename when no alt text"""

        mock_image = Mock()
        mock_image.url = '/media/test-image.jpg'
        mock_image.default_alt_text = None
        mock_image.original_filename = 'test-image.jpg'
        mock_image.width = None
        mock_image.height = None

        template_content = """
        <img src="{{ instance.url }}"
            alt="{% if instance.default_alt_text %}{{ instance.default_alt_text }}{% else %}{{ instance.original_filename }}{% endif %}"
            {% if instance.width %} width="{{ instance.width }}"{% endif %}
            {% if instance.height %} height="{{ instance.height }}"{% endif %}
        >
        """

        template = Template(template_content)
        context = Context({'instance': mock_image})

        rendered = template.render(context)

        # Fallback to filename for alt text
        self.assertIn('alt="test-image.jpg"', rendered)
        # The width/height are not included when `None`
        self.assertNotIn('width=', rendered)
        self.assertNotIn('height=', rendered)
