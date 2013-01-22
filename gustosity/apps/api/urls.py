# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.api.views import api_root,\
    UserList, UserDetail, UserRecipesList, \
    RecipeList, RecipeDetail, LikeRecipe, \
    IngredientList, IngredientDetail,\
    StepList, StepDetail, FollowUser, \
    upload_file

urlpatterns = patterns('',
    url(r'^$', api_root),
    url(r'^users$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^users/(?P<username>[\.\w]+)/follow$', FollowUser.as_view(), name='user-follow'),
    url(r'^recipes$', RecipeList.as_view(), name='recipe-list'),
    url(r'^recipes/(?P<pk>\d+)$', RecipeDetail.as_view(), name='recipe-detail'),
    url(r'^recipes/(?P<pk>\d+)/like$', LikeRecipe.as_view(), name='recipe-like'),
    url(r'^recipes/(?P<username>[\.\w]+)$', UserRecipesList.as_view(), name='user-recipes-list'),
    url(r'^recipes/(?P<pk>\d+)/steps$', StepList.as_view(), name='step-list'),
    url(r'^ingredients$', IngredientList.as_view(), name='ingredient-list'),
    url(r'^ingredients/(?P<pk>\d+)$', IngredientDetail.as_view(), name='ingredient-detail'),
    url(r'^steps$', StepList.as_view(), name='step-list'),
    url(r'^steps/(?P<pk>\d+)$', StepDetail.as_view(), name='step-detail'),
    url(r'^upload$', upload_file, name='step-list-2'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
