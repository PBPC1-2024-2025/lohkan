import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ask_recipe.forms import RecipeForm
from .models import Recipe, RecipeGroup, ChatMessage
import uuid

class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create a test client
        self.client = Client()
        
        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty bytes for test
            content_type='image/jpeg'
        )
        
        # Create a test recipe group
        self.recipe_group = RecipeGroup.objects.create(
            name='Test Recipe Group',
            description='Test Description'
        )
        
        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            servings=4,
            added_by=self.admin_user,
            group=self.recipe_group,
            image='recipe_images/test.jpg'
        )

    def test_ask_recipe_view(self):
        response = self.client.get(reverse('ask_recipe:ask_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask_recipe.html')
        self.assertIn('recipes', response.context)

    def test_create_recipe(self):
        self.client.login(username='admin', password='admin123')
        
        data = {
            'title': 'New Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 45,
            'servings': 6,
            'image': self.test_image
        }
        
        response = self.client.post(reverse('ask_recipe:create_recipe'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recipe.objects.filter(title='New Test Recipe').exists())

    def test_edit_recipe(self):
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Updated Recipe',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions',
            'cooking_time': 60,
            'servings': 8,
            'image': self.test_image
        }
        
        response = self.client.get(
            reverse('ask_recipe:edit_recipe', kwargs={'recipe_id': self.recipe.id})
        )
        self.assertEqual(response.status_code, 200)  # Check if edit page loads
        self.assertTemplateUsed(response, 'partials/edit_recipe.html')

    def test_get_messages(self):
        # Create test message
        message = ChatMessage.objects.create(
            group=self.recipe_group,
            user=self.user,
            message='Test message'
        )
        
        response = self.client.get(
            reverse('ask_recipe:get_messages', kwargs={'group_id': self.recipe_group.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/messages.html')
        self.assertIn('messages', response.context)

    def test_send_message(self):
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'group_id': str(self.recipe_group.id),
            'content': 'Test message content'
        }
        
        response = self.client.post(reverse('ask_recipe:send_message'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChatMessage.objects.filter(message='Test message content').exists())

    def test_delete_group(self):
        response = self.client.post(
            reverse('ask_recipe:delete_group', kwargs={'group_id': self.recipe_group.id})
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertFalse(RecipeGroup.objects.filter(id=self.recipe_group.id).exists())

    def test_delete_message(self):
        # Create test message
        message = ChatMessage.objects.create(
            group=self.recipe_group,
            user=self.user,
            message='Test message to delete'
        )
        
        response = self.client.post(
            reverse('ask_recipe:delete_message', kwargs={'message_id': message.id})
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after deletion
        self.assertFalse(ChatMessage.objects.filter(id=message.id).exists())

    def test_search_recipe(self):
        response = self.client.get(
            reverse('ask_recipe:search_recipe'),
            {'q': 'Test Recipe'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/recipe_list.html')

    def test_search_recipe_no_results(self):
        response = self.client.get(
            reverse('ask_recipe:search_recipe'),
            {'q': 'Nonexistent Recipe'}
        )
        self.assertEqual(response.status_code, 404)

    def test_show_xml(self):
        response = self.client.get(reverse('ask_recipe:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('ask_recipe:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        response = self.client.get(
            reverse('ask_recipe:show_xml_by_id', kwargs={'id': self.recipe.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        response = self.client.get(
            reverse('ask_recipe:show_json_by_id', kwargs={'id': self.recipe.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_json_by_id_not_found(self):
        non_existent_id = uuid.uuid4()
        response = self.client.get(
            reverse('ask_recipe:show_json_by_id', kwargs={'id': non_existent_id})
        )
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        # Clean up any files created during tests
        if self.test_image:
            self.test_image.close()

class RecipeFormTest(TestCase):
    def setUp(self):
        # Buat file gambar test yang sebenarnya dengan beberapa byte
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',  # Minimal GIF file
            content_type='image/jpeg'
        )

    def test_valid_form(self):
        form_data = {
            'title': 'Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 30,
            'servings': 4,
        }
        form = RecipeForm(data=form_data, files={'image': self.test_image})
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug print untuk melihat error spesifik
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_fields(self):
        form_data = {}
        form = RecipeForm(data=form_data, files={'image': self.test_image})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('ingredients', form.errors)
        self.assertIn('instructions', form.errors)
        self.assertIn('cooking_time', form.errors)
        self.assertIn('servings', form.errors)

    def test_invalid_cooking_time(self):
        form_data = {
            'title': 'Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': -1,  # Invalid negative value
            'servings': 4,
        }
        form = RecipeForm(data=form_data, files={'image': self.test_image})
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors)

    def test_invalid_servings(self):
        form_data = {
            'title': 'Test Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 30,
            'servings': 0,  # Invalid zero value
        }
        form = RecipeForm(data=form_data, files={'image': self.test_image})
        self.assertFalse(form.is_valid())
        self.assertIn('servings', form.errors)

class FlutterAPITest(TestCase):
    def setUp(self):
        # Setup yang sama dengan RecipeViewsTest
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        self.client = Client()
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )

    def test_create_recipe_flutter(self):
        data = {
            'title': 'Flutter Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 30,
            'servings': 4,
            'image': self.test_image
        }
        response = self.client.post(reverse('ask_recipe:create_recipe_flutter'), data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Recipe.objects.filter(title='Flutter Recipe').exists())

    def test_update_recipe_flutter(self):
        # Buat resep terlebih dahulu
        group = RecipeGroup.objects.create(name='Test Group')
        recipe = Recipe.objects.create(
            title='Original Recipe',
            ingredients='Original ingredients',
            instructions='Original instructions',
            cooking_time=30,
            servings=4,
            added_by=self.admin_user,
            group=group,
            image='test.jpg'
        )

        # Update resep
        data = {
            'title': 'Updated Flutter Recipe',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions',
            'cooking_time': 45,
            'servings': 6,
            'image': self.test_image
        }
        response = self.client.post(
            reverse('ask_recipe:update_recipe_flutter', kwargs={'recipe_id': recipe.id}),
            data
        )
        self.assertEqual(response.status_code, 200)
        updated_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(updated_recipe.title, 'Updated Flutter Recipe')

    def test_delete_recipe_flutter(self):
        group = RecipeGroup.objects.create(name='Test Group')
        recipe = Recipe.objects.create(
            title='Recipe to Delete',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            servings=4,
            added_by=self.admin_user,
            group=group,
            image='test.jpg'
        )

        response = self.client.delete(
            reverse('ask_recipe:delete_recipe', kwargs={'recipe_id': recipe.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_get_chat_messages(self):
        group = RecipeGroup.objects.create(name='Test Group')
        message = ChatMessage.objects.create(
            group=group,
            user=self.user,
            message='Test message'
        )

        response = self.client.get(
            reverse('ask_recipe:get_chat_messages'),
            {'group_id': group.id}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 1)

    def test_send_chat_message(self):
        self.client.login(username='testuser', password='testpass123')
        group = RecipeGroup.objects.create(name='Test Group')
        
        data = {
            'group_id': str(group.id),
            'message': 'Test message'
        }
        response = self.client.post(
            reverse('ask_recipe:send_chat_message'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_delete_chat_message(self):
        group = RecipeGroup.objects.create(name='Test Group')
        message = ChatMessage.objects.create(
            group=group,
            user=self.user,
            message='Test message'
        )

        response = self.client.delete(
            reverse('ask_recipe:delete_chat_message', kwargs={'message_id': message.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ChatMessage.objects.filter(id=message.id).exists())