# encoding: utf-8
from django.core.management.base import BaseCommand
from apps.recipe.models import Recipe


class Command(BaseCommand):
    help = 'Update all recipe ranks'

    def handle(self, **options):
        for recipe in Recipe.objects.all():
            recipe.update_rank()
