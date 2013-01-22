 # coding=UTF-8
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from apps.food.models import Food, FoodGroup


class FoodAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'food_group')
    list_filter = ('food_group',)
admin.site.register(Food, FoodAdmin)


class FoodGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
admin.site.register(FoodGroup, FoodGroupAdmin)
