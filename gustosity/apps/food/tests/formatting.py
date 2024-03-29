from django.test import TestCase
from apps.food.models import Food, FoodGroup, Unit, Equivalence


class CoreStringTest (TestCase):
    """Test correct string formatting of core models.
    """
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
    ]

    def test_food_string(self):
        """Format Food as a string.
        """
        honey = Food.objects.get(name='honey')
        self.assertEqual(str(honey), 'honey')

    def test_unit_string(self):
        """Format Unit as a string.
        """
        quart = Unit.objects.get(name='quart')
        self.assertEqual(str(quart), 'quart')

    def test_food_group_string(self):
        """Format FoodGroup as a string.
        """
        fruit, created = FoodGroup.objects.get_or_create(name='fruit')
        self.assertEqual(str(fruit), 'fruit')

    def test_equivalence_string(self):
        """Format Equivalence as a string.
        """
        cup_to_pint = Equivalence.objects.get(unit__name='cup', to_unit__name='pint')
        self.assertEqual(str(cup_to_pint), '1 cup = 0.5 pint')
        gallon_to_quart = Equivalence.objects.get(unit__name='gallon', to_unit__name='quart')
        self.assertEqual(str(gallon_to_quart), '1 gallon = 4 quarts')

