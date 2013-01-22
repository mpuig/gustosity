# -*- coding: utf-8 -*-

import datetime
from haystack.indexes import SearchIndex, CharField, MultiValueField
from haystack import site
from apps.recipe.models import Recipe


class RecipeIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    summary = CharField(model_attr='summary')
    #ingredients = CharField(model_attr='ingredients')
    #ingredients = MultiValueField()

    #def prepare_ingredients(self, obj):
    #    return [i.name for i in obj.ingredients.all()]

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Recipe.objects.filter(created_at__lte=datetime.datetime.now())

site.register(Recipe, RecipeIndex)
