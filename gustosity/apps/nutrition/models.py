# -*- coding: utf-8 -*-
from django.db import models


class NutritionInfo (models.Model):
    """Generic nutritional information.
    """
    calories = models.FloatField(default=0)
    fat_calories = models.FloatField(default=0)
    fat = models.FloatField("Fat (g)", default=0)
    carb = models.FloatField("Carb (g)", default=0)
    sodium = models.FloatField("Sodium (mg)", default=0)
    protein = models.FloatField("Protein (g)", default=0)
    cholesterol = models.FloatField("Cholesterol (mg)", default=0)

    class Meta:
        verbose_name_plural = "Nutrition information"

    def __unicode__(self):
        """Format this NutritionInfo as a string.
        """
        string = u"%i calories" % self.calories
        return string

    def full_string(self):
        """Return a string with full details of this NutritionInfo.
        """
        string = "%i calories (%i from fat) " % (self.calories, self.fat_calories)
        string += "%ig fat, %ig carbs, " % (self.fat, self.carb)
        string += "%img sodium, %ig protein, " % (self.sodium, self.protein)
        string += "%img cholesterol" % self.cholesterol
        return string

    def is_empty(self):
        """Return True if this NutritionInfo is empty.
        """
        return all([
            self.calories == 0,
            self.fat_calories == 0,
            self.fat == 0,
            self.carb == 0,
            self.sodium == 0,
            self.protein == 0,
            self.cholesterol == 0,
        ])

    def is_equal(self, other):
        """Return True if this `NutritionInfo` is equal to another,
        False otherwise.
        """
        return all([
            self.calories == other.calories,
            self.fat_calories == other.fat_calories,
            self.fat == other.fat,
            self.carb == other.carb,
            self.sodium == other.sodium,
            self.protein == other.protein,
            self.cholesterol == other.cholesterol,
        ])

    def set_equal(self, other):
        """Set this `NutritionInfo` equal to another, and save.
        """
        self.calories = other.calories
        self.fat_calories = other.fat_calories
        self.fat = other.fat
        self.carb = other.carb
        self.sodium = other.sodium
        self.protein = other.protein
        self.cholesterol = other.cholesterol
        self.save()

    def __add__(self, other):
        """Add this `NutritionInfo` to another, and return the sum.
        """
        return NutritionInfo(
            calories=self.calories + other.calories,
            fat_calories=self.fat_calories + other.fat_calories,
            fat=self.fat + other.fat,
            carb=self.carb + other.carb,
            sodium=self.sodium + other.sodium,
            protein=self.protein + other.protein,
            cholesterol=self.cholesterol + other.cholesterol,
        )

    def __mul__(self, factor):
        """Multiply this `NutritionInfo` by `factor`, and return the product.
        """
        return NutritionInfo(
            calories=factor * self.calories,
            fat_calories=factor * self.fat_calories,
            fat=factor * self.fat,
            carb=factor * self.carb,
            sodium=factor * self.sodium,
            protein=factor * self.protein,
            cholesterol=factor * self.cholesterol
        )
