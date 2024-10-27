from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import RecipeGroup, Recipe, ChatMessage

# Create your tests here.
class RecipeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.recipe_group = RecipeGroup.objects.create(
            name='Test Group',
            description='A group for testing',
            created_by=self.user
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            cooking_time=30,
            servings=4,
            added_by=self.user,
            group=self.recipe_group
        )

    def test_ask_recipe_view(self):
        response = self.client.get(reverse('ask_recipe:ask_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask_recipe.html')

    def test_create_recipe_success(self):
        data = {
            'title': 'New Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Step 1, Step 2',
            'cooking_time': 20,
            'servings': 2,
        }
        response = self.client.post(reverse('ask_recipe:create_recipe'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Recipe')  # Pastikan resep baru ada di response

    def test_get_messages(self):
        response = self.client.get(reverse('ask_recipe:get_messages', kwargs={'group_id': self.recipe_group.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/messages.html')

    def test_send_message(self):
        data = {
            'group_id': self.recipe_group.id,
            'content': 'Hello, this is a test message.'
        }
        response = self.client.post(reverse('ask_recipe:send_message'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, this is a test message.')
    
    def test_delete_group(self):
        response = self.client.post(reverse('ask_recipe:delete_group', kwargs={'group_id': self.recipe_group.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(RecipeGroup.objects.filter(id=self.recipe_group.id).exists())

    def test_delete_message(self):
        message = ChatMessage.objects.create(group=self.recipe_group, user=self.user, message='Test message')
        response = self.client.post(reverse('ask_recipe:delete_message', kwargs={'message_id': message.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(ChatMessage.objects.filter(id=message.id).exists())

    def test_search_recipe(self):
        response = self.client.get(reverse('ask_recipe:search_recipe'), {'q': 'Test Recipe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe')

    def test_show_xml(self):
        response = self.client.get(reverse('ask_recipe:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('ask_recipe:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        response = self.client.get(reverse('ask_recipe:show_xml_by_id', kwargs={'id': self.recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        response = self.client.get(reverse('ask_recipe:show_json_by_id', kwargs={'id': self.recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')