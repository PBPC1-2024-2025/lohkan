import json
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from explore.models import Food


class mainTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.food = Food.objects.create(
            id=uuid4(), name="Test Food", description="A test food item",
            min_price=10, max_price=20, image_link="http://example.com/image.jpg", type="Type1"
        )
        self.food_id = self.food.id

    def test_explore_url_is_exist(self):
        response = self.client.get(reverse('explore:show_explore'))
        self.assertEqual(response.status_code, 302)

    def test_nonexistent_page(self):
        response = self.client.get('/skibidi/')
        self.assertEqual(response.status_code, 404)

    def test_show_explore_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('explore:show_explore'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_show_explore_unauthenticated(self):
        response = self.client.get(reverse('explore:show_explore'))
        self.assertEqual(response.status_code, 302)

    def test_all_to_json(self):
        response = self.client.post(reverse('explore:all_to_json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), Food.objects.count())

    def test_search_food(self):
        response = self.client.post(reverse('explore:search_food'),
                                    json.dumps({'searchText': 'Test'}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['name'], "Test Food")

    def test_filter_food(self):
        response = self.client.post(reverse('explore:filter_food'),
                                    json.dumps({'selectedType': 'Type1'}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['type'], "Type1")

    def test_delete_food(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('explore:delete_food', args=[self.food.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Food.objects.filter(id=self.food.id).exists())

    def test_show_xml(self):
        response = self.client.get(reverse('explore:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('explore:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_add_food_url_is_exist(self):
        response = self.client.get(reverse('explore:add_food'))
        self.assertEqual(response.status_code, 200)

    def test_edit_food_url_is_exist(self):
        response = self.client.get(reverse('explore:edit_food', args=[self.food_id]))
        self.assertIn(response.status_code, [200, 404])  # Adjust if item must exist

    def test_delete_food_url_is_exist(self):
        response = self.client.get(reverse('explore:delete_food', args=[self.food_id]))
        self.assertIn(response.status_code, [302, 404])  # Redirect or Not Found

    def test_show_xml_url_is_exist(self):
        response = self.client.get(reverse('explore:show_xml'))
        self.assertEqual(response.status_code, 200)

    def test_add_food_ajax_url_is_exist(self):
        response = self.client.post(reverse('explore:add_food_ajax'), data={
            'name': 'Sample Food',
            'description': 'Sample Description',
            'min_price': 5,
            'max_price': 15,
            'image_link': 'http://example.com/image.jpg',
            'type': 'SampleType'
        })
        self.assertEqual(response.status_code, 201)

    def test_show_json_url_is_exist(self):
        response = self.client.get(reverse('explore:show_json'))
        self.assertEqual(response.status_code, 200)

    def test_search_food_url_is_exist(self):
        response = self.client.post(reverse('explore:search_food'), data=json.dumps({
            'searchText': 'Sample'
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_all_to_json_url_is_exist(self):
        response = self.client.post(reverse('explore:all_to_json'))
        self.assertEqual(response.status_code, 200)

    def test_filter_food_url_is_exist(self):
        response = self.client.post(reverse('explore:filter_food'), data=json.dumps({
            'selectedType': 'SampleType'
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_food_uses_correct_template(self):
        response = self.client.get(reverse('explore:add_food'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_food.html')

    def test_edit_food_uses_correct_template(self):
        response = self.client.get(reverse('explore:edit_food', args=[self.food_id]))
        self.assertIn(response.status_code, [200, 404])  # Adjust if item must exist
        if response.status_code == 200:  # Check template only if page exists
            self.assertTemplateUsed(response, 'edit_food.html')

    def test_delete_food_redirects_after_deletion(self):
        response = self.client.get(reverse('explore:delete_food', args=[self.food_id]))
        self.assertIn(response.status_code, [302, 404])  # Redirect or Not Found

    def test_show_xml_template(self):
        response = self.client.get(reverse('explore:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_template(self):
        response = self.client.get(reverse('explore:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')