# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.forms.util import ErrorList
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from datetime import datetime

from apps.recipe.models import Recipe, RecipeCategory, Ingredient, Like, _filter_and_sort_recipes
from apps.recipe.forms import RecipeForm


class RecipeDetailViewBase(DetailView):

    """ Base class for all Recipe Detail views """

    context_object_name = 'recipe'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailViewBase, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        recipe = get_object_or_404(Recipe, user__username__iexact=self.kwargs['username'], slug__iexact=self.kwargs['slug'])
        if recipe.is_private and self.request.user != recipe.user:
            raise Http404('Import error raised while fetching module')
        else:
            return recipe


class RecipeDetailView(RecipeDetailViewBase):

    template_name = 'recipe/show_recipe.html'

    def get_object(self):
        object = super(RecipeDetailView, self).get_object()
        key = 'recipe_%d_%s' % (object.pk, self.request.session.session_key)
        if not cache.get(key[:255]):
            cache.set(key, True, 2 * 60)  # count views from the same user with
                                          # more than 2 minutes of difference
            object.total_views += 1
            object.save()

        return object


class RecipeFansView(RecipeDetailViewBase):

    template_name = 'recipe/fans.html'


class RecipeForksView(RecipeDetailViewBase):

    template_name = 'recipe/forks.html'


class RecipesListView(ListView):

    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/list.html'
    paginate_by = 20

    def get_queryset(self):
        params = self.request.GET.dict()
        queryset = Recipe.objects.all()
        self.filterby, self.sortby, queryset = _filter_and_sort_recipes(queryset, self.kwargs, params)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecipesListView, self).get_context_data(**kwargs)
        context['title'] = 'Featured recipes'
        context['categories'] = RecipeCategory.objects.all()
        context['difficulties'] = Recipe.DIFFICULTY_CHOICES
        context['sortby'] = self.sortby
        context['filterby'] = self.filterby
        return context


"""
class RecipesByIngredientListView(ListView):

    context_object_name = 'recipes'
    template_name = 'recipe/list.html'
    paginate_by = 20

    def get_queryset(self):
        return Recipe.objects.filter(ingredients__food__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(RecipesByIngredientListView, self).get_context_data(**kwargs)
        context['title'] = 'Recipes with "%s"' % self.kwargs['slug']
        context['categories'] = RecipeCategory.objects.all()
        context['difficulties'] = Recipe.DIFFICULTY_CHOICES
        return context
"""

"""
class IngredientListView(ListView):

    context_object_name = 'ingredients'
    template_name = 'recipe/ingredients.html'

    def get_queryset(self):
        return Ingredient.objects.annotate(num_recipes=Count('id')).values('name', 'slug', 'num_recipes'
                ).filter(num_recipes__gt=0).order_by('-num_recipes', 'slug')

    def get_context_data(self, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        context['title'] = 'Ingredients'
        context['categories'] = RecipeCategory.objects.all()
        context['difficulties'] = Recipe.DIFFICULTY_CHOICES
        return context
"""

class RecipeCreateView(CreateView):

    form_class = RecipeForm
    model = Recipe
    template_name = 'recipe/form_edit_recipe.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecipeCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecipeCreateView, self).get_context_data(**kwargs)
        context['action'] = 'create'
        context['form_title'] = 'Basic information'
        return context

    def form_valid(self, form):
        from django.db import IntegrityError
        obj = form.save(commit=False)
        obj.user = self.request.user
        try:
            obj.save()
        except IntegrityError, e:
            if str(e).startswith('columns user_id, slug are not unique'):
                form._errors['name'] = ErrorList([u'You already have a recipe with that name.'])
                return super(RecipeCreateView, self).form_invalid(form)
            else:
                raise IntegrityError(e)

        messages.info(self.request, 'New recipe created successfully')
        return HttpResponseRedirect(obj.get_absolute_url())


class RecipeUpdateView(UpdateView):

    form_class = RecipeForm
    model = Recipe
    template_name = 'recipe/form_edit_recipe.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecipeUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.username != self.kwargs['username']:
            raise PermissionDenied
        return get_object_or_404(Recipe, slug=self.kwargs['slug'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        context['action'] = 'update'
        context['form_title'] = 'Edit recipe basic information'
        return context

    def form_valid(self, form):
        from django.db import IntegrityError
        obj = form.save(commit=False)
        obj.user = self.request.user
        try:
            obj.save()
        except IntegrityError:
            from django.forms.util import ErrorList
            form._errors['name'] = ErrorList([u'You already have a recipe with that name.'])
            return super(RecipeCreateView, self).form_invalid(form)

        messages.info(self.request, 'The recipe has been updated successfully')
        return HttpResponseRedirect(obj.get_absolute_url())


class RecipeDeleteView(DeleteView):

    form_class = RecipeForm
    template_name = 'recipe/delete.html'
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RecipeDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe, slug=self.kwargs['slug'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RecipeDeleteView, self).get_context_data(**kwargs)
        messages.info(self.request, 'The recipe has been deleted successfully')
        return context


@login_required
def fork(request, username, slug):
    if Recipe.objects.filter(user=request.user, slug=slug).exists():
        messages.info(request, 'You have forked this recipe before!')
        return HttpResponseRedirect(Recipe.objects.get(user=request.user, slug=slug).get_absolute_url())

    recipe = get_object_or_404(Recipe, user__username__iexact=username, slug=slug)
    new_recipe = recipe.fork(request.user)
    messages.info(request, 'Fork successfully')
    return HttpResponseRedirect(new_recipe.get_absolute_url())
