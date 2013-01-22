# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from actstream.actions import follow, unfollow
from actstream.models import following, followers

from apps.api.serializers import UserSerializer,\
    RecipeSerializer, IngredientSerializer, StepSerializer
from apps.recipe.models import Recipe, Ingredient, Step, Like

from datetime import datetime


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'recipes': reverse('recipe-list', request=request),
        'ingredients': reverse('ingredient-list', request=request),
    })


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of users.
    """
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(id=-1)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single user.
    """
    model = User
    serializer_class = UserSerializer


class UserRecipesList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Recipe
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the recipes for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Recipe.objects.filter(user__username=username)


class RecipeList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Recipe
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single recipe.
    """
    model = Recipe
    serializer_class = RecipeSerializer


class IngredientList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Ingredient
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        This view should return a list of all the ingredients for
        the recipe as determined by the username portion of the URL.
        """
        queryset = Ingredient.objects.all()
        recipe = self.request.QUERY_PARAMS.get('recipe', None)
        if recipe is not None:
            queryset = queryset.filter(recipe__id=recipe)
        return queryset


class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Ingredient
    serializer_class = IngredientSerializer


class StepList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Step
    serializer_class = StepSerializer

    def get_queryset(self):
        """
        This view should return a list of all the steps for
        the recipe as determined by the username portion of the URL.
        """
        queryset = Step.objects.all()
        recipe = self.request.QUERY_PARAMS.get('recipe', None)
        if recipe is not None:
            queryset = queryset.filter(recipe__id=recipe)
        return queryset


class StepDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a list of recipes.
    """
    model = Step
    serializer_class = StepSerializer


@permission_classes((IsAuthenticated, ))
class LikeRecipe(generics.GenericAPIView):
    model = Recipe

    def post(self, request, pk, format=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, recipe=recipe, deleted_at=None)

        if created:
            data = {'message': 'Like successfully'}
        else:
            like.deleted_at = datetime.now()
            like.save()
            data = {'message': 'Unlike successfully'}
        data['count'] = Like.objects.filter(recipe=recipe).count()
        return Response(data)


@permission_classes((IsAuthenticated, ))
class FollowUser(generics.GenericAPIView):

    def post(self, request, username, format=None):
        user_to_follow = get_object_or_404(User, username=username)
        following_list = following(request.user, User)
        if user_to_follow in following_list:
            unfollow(request.user, user_to_follow)
            data = {'message': 'User unfollowed successfully'}
        else:
            follow(request.user, user_to_follow)
            data = {'message': 'User followed successfully'}

        data['count'] = len(followers(user_to_follow))
        return Response(data)


@api_view(['GET', 'POST'])
def upload_file(request):
    if request.method == 'POST':
        instance = Step(original_image=request.FILES['docfile'], description=request.DATA['description'])
        instance.save()
        return Response('uploaded')

    elif request.method == 'GET':
        queryset = Step.objects.all()
        recipe = request.QUERY_PARAMS.get('recipe', None)
        if recipe is not None:
            queryset = queryset.filter(recipe__id=recipe)
        serializer = StepSerializer(queryset)
        return Response(serializer.data)
