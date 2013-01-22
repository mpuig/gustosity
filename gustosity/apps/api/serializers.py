# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers
from apps.recipe.models import Recipe, Ingredient, Step


class UserSerializer(serializers.ModelSerializer):

    #recipes = serializers.ManyHyperlinkedRelatedField(view_name='recipe-detail')

    class Meta:

        model = User
        #fields = 'url', 'username', 'recipes'


class RecipeSerializer(serializers.HyperlinkedModelSerializer):

    ingredients = serializers.ManyRelatedField(source='ingredients')
    steps = serializers.ManyRelatedField(source='steps')
    ingredients_list = serializers.SerializerMethodField('get_ingredients_list')
    steps_list = serializers.SerializerMethodField('get_steps_list')

    class Meta:

        model = Recipe
        fields = (
            'url',
            'name',
            'summary',
            #'user',
            'ingredients',
            'ingredients_list',
            'steps',
            'steps_list',
            'total_likes',
            'total_forks',
            )

    def get_ingredients_list(self, obj):
        return "/api/ingredients?recipe=%d" % obj.pk

    def get_steps_list(self, obj):
        return "/api/steps?recipe=%d" % obj.pk


class IngredientSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.SerializerMethodField('get_ingredient_pk')
    full_name = serializers.SerializerMethodField('get_ingredient_full_name')
    recipe = serializers.HyperlinkedRelatedField(view_name='recipe-detail')

    class Meta:

        model = Ingredient
        exclude = 'slug',

    def get_ingredient_pk(self, obj):
        return obj.pk

    def get_ingredient_full_name(self, obj):
        return obj


class StepSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.SerializerMethodField('get_step_pk')
    recipe = serializers.HyperlinkedRelatedField(view_name='recipe-detail')
    thumb = serializers.SerializerMethodField('get_step_thumb')

    class Meta:

        model = Step
        exclude = 'created_at', 'order', 'original_image'

    def get_step_pk(self, obj):
        return obj.pk

    def get_step_thumb(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        else:
            return None
