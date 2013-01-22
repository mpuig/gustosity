# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import simplejson
from django.utils.encoding import smart_text
import csv

from apps.food.models import FoodGroup, Food

from os.path import join

class Command(BaseCommand):
    help = 'Load food types'

    def handle(self, **options):
        # Step 1: remove all previous data
        FoodGroup.objects.all().delete()
        Food.objects.all().delete()

        """
        # Json from http://gate.foodtree.com/food_types
        filename = join(settings.DJANGO_ROOT, '../fixtures/food_types.json')
        food_types = simplejson.load(open(filename))

        # Step 2: create all new food groups
        for food_type in food_types['food_types']:
            FoodGroup.objects.create(
                name=food_type['name'],
                )

        # Step 3: assing parents
        for foodgroup in FoodGroup.objects.all():
            # Look for the json register
            parents_ids = [f['parent_id'] for f in food_types['food_types'] if f['name'] == foodgroup.name]
            if len(parents_ids) > 0:
                # Get the parents
                parents = [f['name'] for f in food_types['food_types'] if f['id'] == parents_ids[0]]
                if len(parents) > 0:
                    foodgroup.parent = FoodGroup.objects.get(name=parents[0])
                    foodgroup.save()
        """

        # load foods
        filename = join(settings.DJANGO_ROOT, '../fixtures/FoodTypes7Feb2012.csv')
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:
                group = row[1].lower()
                food_group, created = FoodGroup.objects.get_or_create(name=group)
                name = smart_text(row[0].lower())
                try:
                    food, created = Food.objects.get_or_create(name=name, food_group=food_group)
                except:
                    print "Error with %s" % name
