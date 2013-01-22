 # coding=UTF-8
from django.contrib import admin
from apps.account.models import UserProfile

#admin.site.unregister(UserProfile)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_recipes', 'total_recipes_views', 'total_recipes_likes',
        'total_followers', 'total_following', 'last_recipe')
admin.site.register(UserProfile, UserProfileAdmin)
