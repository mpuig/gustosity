 # coding=UTF-8
from django.contrib import admin
from django import forms

from imagekit.admin import AdminThumbnail

from apps.recipe.models import Recipe, Step, RecipeCategory, Ingredient, Like
from apps.food.utils import fraction_to_float


admin.site.register(RecipeCategory)


class StepAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order', 'description', 'recipe', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
admin.site.register(Step, StepAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'recipe', )
admin.site.register(Ingredient, IngredientAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'deleted_at', 'user', 'recipe')
admin.site.register(Like, LikeAdmin)


class QuantityField (forms.Field):
    """A field for entering a quantity. Accepts decimal or fractional values.
    """
    def to_python(self, value):
        return fraction_to_float(value)


class IngredientForm (forms.ModelForm):
    quantity = QuantityField(label="Quantity",
        help_text="""Decimal or fraction value, like "1.75" or "1 3/4".""")

    class Meta:
        model = Ingredient


# Inline forms
class IngredientInline (admin.TabularInline):
    model = Ingredient
    form = IngredientForm
    extra = 8


# Main forms
class RecipeAdmin (admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('created_at', 'name', 'user', 'category', 'total_views',
        'total_likes', 'total_forks', 'rank', 'is_private')
    search_fields = ('name', 'source')
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'category', 'user', 'is_private'),
                ('prep_minutes', 'cook_minutes'),
                'summary',
                ('num_portions', 'portion'),
                ('source'),
            )
        }),
    )

admin.site.register(Recipe, RecipeAdmin)
