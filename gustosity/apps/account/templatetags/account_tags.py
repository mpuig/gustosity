# -*- coding: utf-8 -*-

from django.template import loader, Context, Library
from django.contrib.auth.models import User

from actstream.models import following, user_stream, actor_stream
from apps.recipe.models import Like

register = Library()


@register.simple_tag
def follow_button(user1, user2):
    show_button = user1 != user2
    is_following = show_button and user2 in following(user1, User)
    data = {'show_button': show_button, 'is_following': is_following, 'username': user2.username}
    template = loader.get_template('account/templatetags/follow_button.html')
    return template.render(Context(data))


@register.simple_tag
def show_user_stream(user):
    stream = user_stream(user)
    data = {'stream': stream}
    template = loader.get_template('account/templatetags/stream.html')
    return template.render(Context(data))


@register.simple_tag
def show_actor_stream(user):
    stream = actor_stream(user)
    data = {'stream': stream}
    template = loader.get_template('account/templatetags/stream.html')
    return template.render(Context(data))


@register.filter
def likes(object, user):
    return Like.objects.filter(user=user, recipe=object).count() > 0
