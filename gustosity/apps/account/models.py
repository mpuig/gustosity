# encoding: utf-8
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.validators import MaxLengthValidator

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from django_countries import CountryField

from actstream.models import Follow
from actstream.models import following, followers

from apps.recipe.models import Recipe, Like


class UserProfile(models.Model):
    ACCOUNT_CHOICES = (
        ('bronze', _('Bronze')),
        ('silver', _('Silver')),
        ('gold', _('Gold')),
    )

    user = models.OneToOneField(User, related_name='profile')
    account_type = models.CharField(_('Account type'), max_length=15, choices=ACCOUNT_CHOICES, default='bronze')
    about_me = models.TextField(_('about me'), validators=[MaxLengthValidator(300)], blank=True,
        help_text='Max length 300 chars')
    country = CountryField(blank=True, null=True)
    website = models.URLField(_('Website URL'), verify_exists=False, blank=True)
    twitter = models.CharField(_('Twitter username'), max_length=255, blank=True)

    photo = models.ImageField(u"A personal image displayed in your profile.", upload_to='profiles',
        blank=True, null=True)
    avatar_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(200, 200)], image_field='photo',
            format='JPEG', options={'quality': 90})
    avatar_mini = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(40, 40)], image_field='photo',
            format='JPEG', options={'quality': 90})

    # denormalized counters for user's statistics
    total_views = models.PositiveIntegerField(_("Total profile views"),
        default=0, db_index=True, editable=False)
    total_recipes = models.PositiveIntegerField(_("Total recipe"),
        default=0, db_index=True, editable=False)
    total_recipes_views = models.PositiveIntegerField(_("Sum of all views for user recipes"),
        default=0, db_index=True, editable=False)
    total_recipes_likes = models.PositiveIntegerField(_("Sum of all likes for user recipes"),
        default=0, db_index=True, editable=False)
    total_followers = models.PositiveIntegerField(_("Followers"),
        default=0, db_index=True, editable=False)
    total_following = models.PositiveIntegerField(_("Following"),
        default=0, db_index=True, editable=False)
    last_recipe = models.DateTimeField(_("Total user followers"),
        blank=True, null=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ('show_user', [self.username])

    def get_avatar_url(self):
        from social_auth.models import UserSocialAuth
        if self.photo:
            return self.avatar_thumbnail.url
        elif UserSocialAuth.objects.filter(provider='facebook', user=self.user).count() > 0:
            instance = UserSocialAuth.objects.filter(provider='facebook').get(user=self.user)
            return 'http://graph.facebook.com/%s/picture?type=large' % instance.uid
        else:
            return "/static/images/chef.jpg"

    def get_rating_average(self):
        if self.total_recipes > 0:
            return self.total_recipes_likes / self.total_recipes
        else:
            return 0

    def get_top_rated_recipes(self):
        return Recipe.objects.filter(user=self.user).order_by('total_likes')[:3]

    def get_published_recipes(self):
        return self.total_recipes

    def get_newest_recipe(self):
        try:
            return Recipe.objects.filter(user=self.user).latest()
        except:
            return None

    def get_likes_count(self):
        return Like.objects.filter(user=self.user).count()

    def update_totals(self):
        totals = Recipe.objects.filter(user=self.user).aggregate(Sum('total_likes'), Sum('total_views'))
        if totals:
            self.total_recipes_likes = totals['total_likes__sum']
            self.total_recipes_views = totals['total_views__sum']
            self.total_recipes = Recipe.objects.filter(user=self.user).count()
            self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Follow)
def user_follows(sender, instance, created, **kwargs):
    # Update users counters
    instance.user.profile.total_following =\
        len(following(instance.user, User))
    instance.user.profile.save()

    instance.follow_object.profile.total_followers =\
        len(followers(instance.follow_object))
    instance.follow_object.profile.save()


@receiver(post_delete, sender=Follow)
def user_deletes_recipe(sender, instance, using, **kwargs):
    # Update users counters
    instance.user.profile.total_following =\
        len(following(instance.user, User))
    instance.user.profile.save()

    instance.follow_object.profile.total_followers =\
        len(followers(instance.follow_object))
    instance.follow_object.profile.save()
