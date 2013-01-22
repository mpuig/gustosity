# encoding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from apps.recipe.models import Recipe, RecipeCategory, Like, Step


class RecipeTestCase(TestCase):
    fixtures = ["test_fixtures_user.json"]

    def setUp(self):
        self.user = User.objects.all()[2]

    def test_new_recipe(self):
        recipe = Recipe.objects.create(
            name="Nullam Condimentum",
            summary="Vestibulum id ligula porta felis euismod semper.",
            difficulty=Recipe.DIFFICULTY_CHOICES[0],
            category=RecipeCategory.objects.all().latest(),
            servings=4,
            prep_minutes=90,
            cook_minutes=30,
            user=self.user
        )
        self.assertEqual(recipe.name, 'Nullam Condimentum')

    def test_view_recipe(self):
        response = self.client.get('/customer/details/')
        self.assertEqual(response.status_code, 200)