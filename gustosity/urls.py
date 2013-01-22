from django.conf import settings
from django.contrib import admin
#from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from apps.account.views import UserLikesView, UserActivityView,\
    UserView, UserFollowingView, UserFollowersView
from apps.recipe.views import RecipesListView,\
    RecipeDetailView, RecipeCreateView, RecipeDeleteView,\
    RecipeUpdateView, RecipeForksView, RecipeFansView

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # API
    (r'^api/', include('apps.api.urls')),

    (r'^search/', include('haystack.urls')),

    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # flatpages
    (r'^help/', include('django.contrib.flatpages.urls')),

    # django-registration
    (r'^account/', include('registration.backends.default.urls')),

    # Edit profile
    url(r'^account/edit/$', 'apps.account.views.edit', name='edit_profile'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),

    # app urls
    (r'^activity/', include('actstream.urls')),

    # Browse recipes section
    # url(r'^r/ingredients/(?P<slug>[-\w]+)/$', RecipesByIngredientListView.as_view(), name='recipes_byingredient'),
    # url(r'^r/ingredients/$', IngredientListView.as_view(), name='view_ingredients'),
    url(r'^r/(?P<filter>[-\w]+)/$', RecipesListView.as_view(), name='recipes_byfilter'),
    url(r'^r/', RecipesListView.as_view(), name='recipe_list'),

    # Upload files
    url(r'^upload/$', 'apps.file_uploader.views.upload'),

    # Contact form
    url(r'^contact/', include("apps.contact_form.urls", namespace="contact_form")),

    # Pricing plans
    url(r'^plans/$', direct_to_template, {'template': 'plans.html'}, name='plans'),

    url(r'', include('social_auth.urls')),

    # User recipes section
    url(r'^new/$', RecipeCreateView.as_view(), name='recipe_new'),
    url(r'^(?P<username>[\.\w]+)/$', UserView.as_view(), name='show_user'),
    url(r'^(?P<username>[\.\w]+)/likes/$', UserLikesView.as_view(), name='user_likes'),
    url(r'^(?P<username>[\.\w]+)/following/$', UserFollowingView.as_view(), name='user_following'),
    url(r'^(?P<username>[\.\w]+)/followers/$', UserFollowersView.as_view(), name='user_followers'),
    url(r'^(?P<username>[\.\w]+)/activity/$', UserActivityView.as_view(), name='user_activity'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(), name='recipe_show'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/delete/$', RecipeDeleteView.as_view(), name='recipe_delete'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/fans/$', RecipeFansView.as_view(), name='recipe_fans'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/forks/$', RecipeForksView.as_view(), name='recipe_forks'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/edit/$', RecipeUpdateView.as_view(), name='recipe_edit'),
    url(r'^(?P<username>[\.\w]+)/(?P<slug>[-\w]+)/fork/$', 'apps.recipe.views.fork', name='ajax-recipe_fork'),

    # Home
    url(r'^$', 'apps.account.views.home', name='home'),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, 'show_indexes': True}))
