# encoding: utf-8
from django.db import models
from django.db.models.signals import post_save, pre_delete, post_syncdb
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files import File
from django.conf.global_settings import LANGUAGES

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from actstream import action

from apps.food.models import Unit
#from apps.food.utils import format_food_unit
from apps.food.helpers import group_by_category
from apps.sluggable.models import SluggableModel

import datetime


class RecipeCategory(SluggableModel):
    """A category of recipe.
    Examples: entree, dessert, side dish.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Recipe categories'
        get_latest_by = 'name'

    def __unicode__(self):
        return u'%s' % self.name


def _filter_and_sort_recipes(queryset, kwargs, params):
    SORT_RECIPES_DICT = {
        'rank': '-rank',
        'likes': '-total_likes',
        'views': '-total_views',
        'forks': '-total_forks'
        }
    filterby = kwargs.get('filter', 'default')
    if RecipeCategory.objects.filter(slug=filterby).exists():
        queryset = queryset.filter(category__slug__iexact=filterby)
    elif filterby in Recipe.DIFFICULTIES:
        queryset = queryset.filter(difficulty=filterby)
    sortby = params.get('sortby', 'default')
    if sortby in SORT_RECIPES_DICT:
        queryset = queryset.order_by(SORT_RECIPES_DICT[sortby])

    return filterby, sortby, queryset


class PublicRecipesManager(models.Manager):
    def get_query_set(self):
        return super(PublicRecipesManager, self).get_query_set().filter(is_private=False)


class Recipe(SluggableModel):
    DIFFICULTY_CHOICES = (
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('difficult', _('Difficult')),
    )
    DIFFICULTIES = [cat[0] for cat in DIFFICULTY_CHOICES]
    name = models.CharField(max_length=255)
    original = models.ForeignKey('self', blank=True, null=True,
        on_delete=models.SET_NULL, editable=False)
    summary = models.TextField(_(u"Summary"),
        help_text=_(u"Summarize in a sentence or two what this recipe is about."))
    category = models.ForeignKey(RecipeCategory, blank=True, null=True,
        help_text=_("A category of recipe. Examples: entree, dessert, side dish."))
    difficulty = models.CharField(_(u"Level of difficulty"),
        max_length=50, blank=True, null=True,
        choices=DIFFICULTY_CHOICES,
        help_text=_(u"Be honest!"))
    servings = models.PositiveIntegerField(_(u"Servings"),
        blank=True, null=True,
        help_text=_(u"For how many people is this list of ingredients?"))
    tips = models.TextField(_(u"Recipe tips"),
        blank=True, null=True,
        help_text=_(u"Do you have some tips to comment?"))
    prep_minutes = models.IntegerField(_(u"Preparation time"),
        blank=True, null=True,
        help_text=_(u"Time spent gathering, preparing, and mixing the ingredients, in minutes."))
    inactive_prep_minutes = models.IntegerField(_(u"Inactive preparation time"),
        blank=True, null=True,
        help_text=_(u"Time spent waiting, for example when meat is marinating, or bread dough is rising. In minutes."))
    cook_minutes = models.IntegerField(_(u"Cooking time"),
        blank=True, null=True,
        help_text=_(u"Time spent actually cooking or baking, in minutes."))
    num_portions = models.IntegerField("Number of portions", default=1, blank=True, null=True)
    portion = models.CharField(_("Portion name"), max_length=100, blank=True, null=True,
        help_text=_(u"Serving or portion names for recipe yields. Examples: muffin, roll, loaf, serving."))
    source = models.URLField(_('Original source'),
        blank=True, null=True,
        help_text=_('Did you find this recipe somewhere? Be nice with the author.'))
    language = models.CharField(max_length=100, choices=LANGUAGES, blank=True, null=True,
        help_text=_('The language you use to describe the recipe'))
    user = models.ForeignKey(User, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    original_image = models.ImageField(u"Main image", upload_to='photos',
        blank=True, null=True)
    formatted_image = ImageSpecField(image_field='original_image', format='JPEG',
            options={'quality': 90})
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(200, 200)], image_field='original_image',
            format='JPEG', options={'quality': 90})
    mini_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(90, 70)], image_field='original_image',
            format='JPEG', options={'quality': 90})
    cover = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
            ResizeToFill(400, 400)], image_field='original_image',
            format='JPEG', options={'quality': 90})

    rank = models.PositiveIntegerField(_(u"Rank"), default=0, editable=False)

    # denormalized counters for recipe statistics
    total_views = models.PositiveIntegerField(_("Total recipe's views"),
        blank=True, null=True, default=0, db_index=True, editable=False)
    total_likes = models.PositiveIntegerField(_("Total recipe's likes"),
        blank=True, null=True, default=0, db_index=True, editable=False)
    total_forks = models.PositiveIntegerField(_("Total recipe's forks"),
        blank=True, null=True, default=0, db_index=True, editable=False)

    # Managers
    objects = PublicRecipesManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'gustosity_recipes'
        ordering = ['-created_at']
        get_latest_by = 'created_at'
        unique_together = ('user', 'slug')

    def __unicode__(self):
        return u'%s' % self.name

    def ingredient_groups(self):
        """Return a list of ``(category, [ingredients])`` for this recipe.
        ``category`` is ``None`` for any ingredients without a defined category.
        """
        return group_by_category(self.ingredients.all())

    def update_rank(self):
        likes = Like.recents.filter(recipe=self).count()
        # TODO: afegir paràmetre views i una fòrmula amb decay
        self.rank = likes
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('recipe_show', [self.user.username, self.slug])

    def get_other_same_chef(self):
        return Recipe.objects.\
            exclude(pk=self.pk).\
            filter(user=self.user)

    def get_other_same_category(self):
        return Recipe.objects.\
            exclude(pk=self.pk).\
            exclude(user=self.user).\
            filter(category=self.category)

    def get_fans(self):
        users_list = Like.objects.\
            filter(recipe=self, deleted_at=None).\
            values_list('user', flat=True)
        return User.objects.filter(pk__in=users_list)

    def get_forks(self):
        return Recipe.objects.filter(original=self)

    def fork(self, new_user):
        original = Recipe.objects.get(pk=self.pk)
        new_recipe = self
        new_recipe.pk = None
        new_recipe.original = original
        new_recipe.user = new_user
        new_recipe.total_views = 0
        new_recipe.total_likes = 0
        new_recipe.total_forks = 0
        file = File(open(original.original_image.path))
        new_recipe.original_image.save(original.original_image.path, file)

        new_recipe.save()
        for step in original.steps.all():
            step.fork(new_recipe)

        for ingredient in original.ingredients.all():
            ingredient.fork(new_recipe)

        original.total_forks += 1
        original.save()
        return new_recipe


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps')
    description = models.TextField(_(u"Step description"),
        help_text=_(u"Step description"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    order = models.PositiveSmallIntegerField(blank=True, null=True,
        default=0, db_index=True, editable=False)

    original_image = models.ImageField(u"Main image", upload_to='photos',
        blank=True, null=True)
    formatted_image = ImageSpecField(image_field='original_image', format='JPEG',
            options={'quality': 90})
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(200, 200)], image_field='original_image',
            format='JPEG', options={'quality': 90})
    mini_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(90, 70)], image_field='original_image',
            format='JPEG', options={'quality': 90})
    cover = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
            ResizeToFill(400, 400)], image_field='original_image',
            format='JPEG', options={'quality': 90})

    class Meta:
        db_table = 'gustosity_recipe_steps'
        ordering = ['order', '-created_at']
        get_latest_by = 'order'

    def __unicode__(self):
        return u'Step %d - %s' % (self.pk, self.description)

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                steps = Step.objects.filter(recipe=self.recipe)
                if steps:
                    self.order = steps.latest().order + 1
        except ObjectDoesNotExist:
            pass

        return super(Step, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('recipe_show', [self.recipe.user.username, self.recipe.slug])

    def fork(self, new_recipe):
        new_step = self
        new_step.pk = None
        new_step.recipe = new_recipe
        new_step.save()


class Ingredient(models.Model):
    """A quantity of food used in a recipe.
    """
    recipe = models.ForeignKey(Recipe, related_name='ingredients')
    name = models.CharField(_("Name (and quantities)"), max_length=100)
    base_name = models.CharField(_("Base name (i.e. potato)"), max_length=100, blank=True, null=True)
    quantity = models.FloatField(default=0.0, blank=True, null=True)
    # unit = models.ForeignKey(Unit, blank=True, null=True)
    optional = models.BooleanField(default=False)

    def __unicode__(self):
        #string = format_food_unit(self.quantity, self.unit, self.name)
        string = self.name
        if self.optional:
            string += " (optional)"
        return string

    def fork(self, new_recipe):
        new_ingredient = self
        new_ingredient.pk = None
        new_ingredient.recipe = new_recipe
        new_ingredient.save()


class LikesManager(models.Manager):
    def get_query_set(self):
        return super(LikesManager, self).get_query_set().filter(deleted_at__isnull=True)


class RecentLikesManager(LikesManager):
    def get_query_set(self):
        now = datetime.datetime.today()
        recent_delta = datetime.timedelta(days=15)
        recent = now - recent_delta
        return super(RecentLikesManager, self).get_query_set().filter(created_at__gte=recent)


class Like(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Managers
    all_objects = models.Manager()
    objects = LikesManager()
    recents = RecentLikesManager()

    class Meta:
        db_table = 'gustosity_likes'
        ordering = ['-pk']

    def __unicode__(self):
        return u'User %s likes %s' % (self.user, self.recipe)


@receiver(post_save, sender=Recipe)
def user_creates_recipe(sender, instance, created, **kwargs):
    if not instance.is_private:
        if created and instance.original:
            action.send(instance.user, verb='forked', target=instance.original)
        elif created:
            action.send(instance.user, verb='created recipe', target=instance)

        instance.user.profile.update_totals()


@receiver(pre_delete, sender=Recipe)
def user_deletes_recipe(sender, instance, using, **kwargs):
    if not instance.is_private:
        instance.user.profile.update_totals()


@receiver(post_save, sender=Like)
def user_likes_recipe(sender, instance, created, **kwargs):
    recipe = instance.recipe
    action.send(instance.user, verb='liked', target=recipe)
    recipe.total_likes = Like.objects.filter(recipe=recipe).count()
    recipe.save()
    recipe.update_rank()


@receiver(post_syncdb)
def create_default_project(created_models, verbosity=2, **kwargs):
    if RecipeCategory in created_models and RecipeCategory.objects.all().count() == 0:
        for name in ['Dinner', 'Lunch', 'Breakfast', 'Drinks', 'Grilling', \
        'Small plates', 'Soups', 'Salads', 'Baking & desserts']:
            RecipeCategory.objects.create(name=name)
