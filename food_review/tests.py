from django.test import TestCase
from django.urls import reverse
from food_review.forms import ReviewEntryForm
from food_review.models import ReviewEntry
from django.contrib.auth.models import User
import xml.etree.ElementTree as ET  # Import the XML parsing module

class ReviewEntryTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create some reviews
        self.review1 = ReviewEntry.objects.create(
            name="Spaghetti",
            food_type="Main Course",
            rating=4,
            user=self.user,
            comments="Delicious!"
        )
        self.review2 = ReviewEntry.objects.create(
            name="Burger",
            food_type="Snacks",
            rating=5,
            user=self.user,
            comments="Perfect snack!"
        )
        self.review3 = ReviewEntry.objects.create(
            name="Ice Cream",
            food_type="Dessert",
            rating=3,
            user=self.user,
            comments="Very good!"
        )
        self.review4 = ReviewEntry.objects.create(
            name="Pizza",
            food_type="Main Course",
            rating=5,
            user=self.user,
            comments="Best pizza ever!"
        )
        
    def test_page_review_without_filters(self):
        response = self.client.get(reverse('food_review:page_review'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['top_rated_dishes']), 3)

    def test_page_review_with_search_filter(self):
        response = self.client.get(reverse('food_review:page_review'), {'search': 'pizza'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 1)
        self.assertEqual(response.context['reviews'][0]['name'], 'Pizza')

    def test_page_review_with_type_filter(self):
        response = self.client.get(reverse('food_review:page_review'), {'type': 'Main Course'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 2)

    def test_form_valid_data(self):
        form = ReviewEntryForm(data={
            'name': 'Lasagna',
            'food_type': 'Main Course',
            'rating': 5,
            'comments': 'Excellent dish!'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # Test with missing name and food_type which are required fields
        form = ReviewEntryForm(data={
            'rating': 5,
            'comments': 'Excellent dish!'
        })
        self.assertFalse(form.is_valid())

    def test_form_no_data(self):
        # Test form with no data
        form = ReviewEntryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Expecting errors for the four required fields

    # New tests for XML and JSON views
    def test_show_xml(self):
        response = self.client.get(reverse('food_review:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode('utf-8')
        root = ET.fromstring(content)
        names = [field.text for field in root.findall(".//field[@name='name']")]
        self.assertIn('Spaghetti', names)
        self.assertIn('Burger', names)

    def test_show_json(self):
        response = self.client.get(reverse('food_review:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        content = response.json()
        names = [entry['fields']['name'] for entry in content]
        self.assertIn('Spaghetti', names)
        self.assertIn('Burger', names)

    def test_show_xml_by_id(self):
        response = self.client.get(reverse('food_review:show_xml_by_id', args=[self.review1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode('utf-8')
        root = ET.fromstring(content)
        names = [field.text for field in root.findall(".//field[@name='name']")]
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'Spaghetti')

    def test_show_json_by_id(self):
        response = self.client.get(reverse('food_review:show_json_by_id', args=[self.review1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        content = response.json()
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['fields']['name'], 'Spaghetti')
