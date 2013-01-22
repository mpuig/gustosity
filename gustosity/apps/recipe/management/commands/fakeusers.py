import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.recipe.management.commands.data import FIRST_NAMES, LAST_NAMES, FREE_EMAIL

rand = lambda x: random.choice(x.split())


def get_user():
    first_name = rand(FIRST_NAMES)
    last_name = rand(LAST_NAMES)
    username = ("%s%s" % (first_name, last_name)).lower().replace("'", "")
    password = 'password'
    email = "%s@%s" % (username, rand(FREE_EMAIL))
    return [first_name, last_name, username, email, password]


class Command(BaseCommand):
    help = 'Creates a bunch of random users'

    def handle(self, **options):
        for i in range(20):
            user = get_user()
            u = User.objects.create(
                first_name=user[0],
                last_name=user[1],
                username=user[2],
                email=user[3],
                )
            u.set_password(user[4])
