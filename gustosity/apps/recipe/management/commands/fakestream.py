# encoding: utf-8
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
from django.core.files import File
from django.utils.encoding import smart_text
from django.conf.global_settings import LANGUAGES

from actstream.actions import follow, unfollow
from actstream.models import following
from apps.recipe.models import Recipe, RecipeCategory, Like, Step
from apps.food.models import Food

SERVINGS = range(1, 15)

CATEGORIES = RecipeCategory.objects.order_by('?')

INGREDIENTS_TOP = list(Food.objects.order_by('?').values_list('id', flat=True)[:10])


def get_recipe():
    INGREDIENTS = Food.objects.exclude(id__in=INGREDIENTS_TOP).order_by('?').values_list('name', flat=True)[:random.randint(2, 10)]
    return {
        'ingredients': INGREDIENTS,
        'summary': '\n\n'.join(lorem_ipsum.paragraphs(random.randint(0, 2), False)),
        'name': lorem_ipsum.words(random.randint(2, 6), False).title(),
        'difficulty': random.choice(Recipe.DIFFICULTY_CHOICES)[0],
        'category': random.choice(CATEGORIES),
        'servings': random.choice(SERVINGS),
        'prep_minutes': random.choice(range(10, 150, 5)),
        'inactive_prep_minutes': random.choice(range(0, 150, 5)),
        'cook_minutes': random.choice(range(10, 150, 5)),
        'language': random.choice(LANGUAGES),
        'is_private': random.choice([True, False])
    }


def get_steps():
    return '\n\n'.join([lorem_ipsum.words(random.randint(5, 50), False) for i in range(random.randint(1, 5))])


def make_random_recipes():
    print "make random recipes"
    for i in range(random.randint(5, 20)):
        user = User.objects.all().order_by('?')[0]
        recipe = get_recipe()
        r = Recipe.objects.create(
            name=recipe['name'],
            summary=recipe['summary'],
            difficulty=recipe['difficulty'],
            category=recipe['category'],
            servings=recipe['servings'],
            prep_minutes=recipe['prep_minutes'],
            cook_minutes=recipe['cook_minutes'],
            language=recipe['language'],
            is_private=recipe['is_private'],
            user=user,
            total_views=random.randint(0, 100),
        )

        for name in recipe['ingredients']:
            try:
                r.ingredients.create(name=smart_text(name), quantity=random.randint(0, 10))
            except:
                pass

        for name in Food.objects.filter(id__in=INGREDIENTS_TOP)[:random.randint(5, 10)]:
            try:
                r.ingredients.create(name=smart_text(name), quantity=random.randint(0, 10))
            except:
                pass

        # add cover image to recipe
        filename = 'fixtures/img_%d.png' % random.randint(0, 10)
        file = File(open(filename))
        r.original_image = file
        r.original_image.save(filename, file)
        r.save()

        for j in range(random.randint(1, 10)):
            s = Step.objects.create(
                description=get_steps(),
                recipe=r,
            )
            # add cover image to the step
            filename = 'fixtures/img_%d.png' % random.randint(0, 10)
            file = File(open(filename))
            s.original_image = file
            s.original_image.save(filename, file)
            s.save()


def make_random_follows(max_users):
    print "make random follows"
    some_users = User.objects.all().order_by('?')[:random.randint(0, max_users)]
    for user in some_users:
        for u in User.objects.exclude(pk=user.pk).order_by('?')[:random.randint(0, 10)]:
            follow(user, u)


def make_random_unfollows(max_users):
    print "make random unfollows"
    some_users = User.objects.all().order_by('?')[:random.randint(0, max_users)]
    for user in some_users:
        following_list = following(user, User)
        for u in following_list[:random.randint(0, len(following_list))]:
            unfollow(user, u)


def make_random_likes():
    print "make random likes"
    for i in range(random.randint(0, 20)):
        recipe = Recipe.objects.all().order_by('?')[0]
        user = User.objects.exclude(pk=recipe.user.pk).order_by('?')[0]
        Like.objects.create(
            user=user,
            recipe=recipe,
            deleted_at=None
            )


def make_random_forks():
    print "make random forks"
    for i in range(random.randint(0, 20)):
        recipe = Recipe.objects.all().order_by('?')[0]
        user = User.objects.exclude(pk=recipe.user.pk).order_by('?')[0]
        try:
            recipe.fork(user)
        except:
            print "Recipe: %s not forked by %s" % (recipe.name, user.username)


class Command(BaseCommand):
    help = 'Creates a random activity'

    def handle(self, **options):
        max_users = User.objects.all().count()
        for i in range(3):
            print i
            make_random_follows(max_users)
            make_random_unfollows(max_users)
            make_random_recipes()
            make_random_likes()
            make_random_forks()
            # unlikes
