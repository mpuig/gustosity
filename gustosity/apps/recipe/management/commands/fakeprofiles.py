# -*- coding: utf-8 -*-

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum

from apps.account.models import UserProfile
from apps.recipe.management.commands.data import TLDS
from django_countries.countries import COUNTRIES

rand = lambda x: random.choice(x.split())


def get_profile():
    about_me = '\n'.join(lorem_ipsum.paragraphs(random.randint(1, 3), False))
    country_code, name = random.choice(COUNTRIES)
    company_name = lorem_ipsum.words(random.randint(1, 3), False).title()
    website = 'http://www.%s.%s' % (company_name.lower().replace(' ', ''), random.choice(TLDS))
    return [about_me, country_code, company_name, website]


class Command(BaseCommand):

    help = 'Creates a bunch of random profiles'

    def handle(self, **options):
        UserProfile.objects.all().delete()
        for user in User.objects.all():
            profile = get_profile()
            UserProfile.objects.create(user=user, website=profile[3], about_me=(profile[0])[:300],
                                       country=profile[1], twitter=user.username)
