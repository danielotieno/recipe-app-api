from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """Test available ingredients which are public."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving ingredient."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """Test the private user Ingredients API."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving ingredient list."""
        Ingredient.objects.create(user=self.user, name='Cucumber')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
