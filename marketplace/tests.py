from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Listing

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

class ListingDeactivateTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.user = get_user_model().objects.create_user(
            username="seller@example.com",
            email="seller@example.com",
            password="testpass123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="testpass123"
        )
        self.listing = Listing.objects.create(
            seller=self.user,
            category=self.category,
            title="Laptop",
            description="Good condition",
            price="100.00",
            pickup_location="Campus",
            status="Available",
        )

    def test_seller_can_deactivate_listing(self):
        self.client.login(email="seller@example.com", password="testpass123")
        response = self.client.post(
            reverse('marketplace:deactivate_listing', args=[self.listing.id])
        )
        self.listing.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.listing.status, "Inactive")

    def test_non_seller_cannot_deactivate_listing(self):
        self.client.login(email="other@example.com", password="testpass123")
        response = self.client.post(
            reverse('marketplace:deactivate_listing', args=[self.listing.id])
        )
        self.listing.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.listing.status, "Available")

    def test_staff_user_can_deactivate_listing(self):
        staff_user = get_user_model().objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.client.login(email="admin@example.com", password="testpass123")
        response = self.client.post(
            reverse('marketplace:deactivate_listing', args=[self.listing.id])
        )
        self.listing.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.listing.status, "Inactive")