 # coding=UTF-8
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.context import RequestContext
from django.views.generic import ListView
from actstream.models import following, followers
from apps.account.forms import UserProfileForm
from apps.recipe.models import Recipe, RecipeCategory, _filter_and_sort_recipes


def home(request):
    if not request.user.is_authenticated():
        recipes = Recipe.objects.all()[:9]
        categories = RecipeCategory.objects.all()
        difficulties = Recipe.DIFFICULTY_CHOICES

        data = {
            'recipes': recipes,
            'categories': categories,
            'difficulties': difficulties,
        }
        return render_to_response('home.html',
            data, RequestContext(request))
    else:
        return HttpResponseRedirect(
            reverse('show_user', kwargs={
                'username': request.user.username
                })
        )


@login_required
def edit(request):
    form = UserProfileForm(request.POST or None, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.info(request, 'User account saved successfully')
        return HttpResponseRedirect(
            reverse('show_user', kwargs={
                'username': request.user.username
                })
        )
    data = {
        'form': form
    }
    return render_to_response('account/edit.html', data, RequestContext(request))


class UserView(ListView):
    context_object_name = "recipes"
    template_name = "account/show_user.html"

    def get_queryset(self):
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        params = self.request.GET.dict()
        self.filterby, self.sortby, queryset = _filter_and_sort_recipes(
            user.recipes.all(), self.kwargs, params)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['chef'] = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        context['extra_title'] = u"recipes"
        context['sortby'] = self.sortby
        context['filterby'] = self.filterby
        return context


class UserActivityView(ListView):
    context_object_name = "recipes"
    template_name = "account/activity.html"

    def get_queryset(self):
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        return user.recipes.all()

    def get_context_data(self, **kwargs):
        context = super(UserActivityView, self).get_context_data(**kwargs)
        context['chef'] = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        context['extra_title'] = u"activity"
        return context


class UserLikesView(ListView):
    context_object_name = "recipes"
    template_name = "account/likes.html"

    def get_queryset(self):
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        return Recipe.objects.filter(like__user=user, like__deleted_at=None)

    def get_context_data(self, **kwargs):
        context = super(UserLikesView, self).get_context_data(**kwargs)
        context['chef'] = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        context['extra_title'] = u"likes"
        return context


class UserFollowingView(ListView):
    context_object_name = "users"
    template_name = "account/follows.html"

    def get_queryset(self):
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        return following(user, User)

    def get_context_data(self, **kwargs):
        context = super(UserFollowingView, self).get_context_data(**kwargs)
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        context['chef'] = user
        context['title'] = "Users %s's following" % user
        context['extra_title'] = "following"
        return context


class UserFollowersView(ListView):
    context_object_name = "users"
    template_name = "account/follows.html"

    def get_queryset(self):
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        return followers(user)

    def get_context_data(self, **kwargs):
        context = super(UserFollowersView, self).get_context_data(**kwargs)
        user = get_object_or_404(User,
            username__iexact=self.kwargs['username'])
        context['chef'] = user
        context['title'] = "Users following %s" % user
        context['extra_title'] = "followers"
        return context
