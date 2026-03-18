from django.test import TestCase
from django.urls import reverse
from .models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        # Set up initial data for the test
        Category.objects.create(name="Textbooks")

    def test_category_creation(self):
        # Check if the category was successfully created and retrieved
        cats = Category.objects.filter(name="Textbooks")
        self.assertTrue(cats.exists())

class IndexViewTest(TestCase):
    def test_index_view_status_code(self):
        # Verify that the homepage loads successfully (HTTP 200)
        response = self.client.get(reverse('marketplace:index'))
        self.assertEqual(response.status_code, 200)

    def test_post_item_redirects_if_not_logged_in(self):
        # Ensure unauthenticated users are redirected (HTTP 302)
        response = self.client.get(reverse('marketplace:post_item'))
        self.assertEqual(response.status_code, 302)