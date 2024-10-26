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