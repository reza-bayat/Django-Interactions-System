from django import template
from django.db import models
from django.contrib.contenttypes.models import ContentType

from interactions.models import Bookmark, Like, Rating

register = template.Library()

@register.inclusion_tag('interactions/like_button.html', takes_context=True)
def like_button(context, obj):
    request = context['request']
    content_type = ContentType.objects.get_for_model(obj)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        ).exists()
    like_count = Like.objects.filter(content_type=content_type, object_id=obj.id).count()
    return {
        'obj': obj,
        'content_type': content_type,
        'liked': liked,
        'like_count': like_count
    }

@register.inclusion_tag('interactions/bookmark_button.html', takes_context=True)
def bookmark_button(context, obj):
    request = context['request']
    content_type = ContentType.objects.get_for_model(obj)
    bookmarked = False
    if request.user.is_authenticated:
        bookmarked = Bookmark.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        ).exists()
    return {
        'obj': obj,
        'content_type': content_type,
        'bookmarked': bookmarked
    }

@register.inclusion_tag('interactions/rating_widget.html', takes_context=True)
def rating_widget(context, obj):
    request = context['request']
    content_type = ContentType.objects.get_for_model(obj)
    user_rating = None
    if request.user.is_authenticated:
        rating_obj = Rating.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        ).first()
        user_rating = rating_obj.score if rating_obj else 0

    avg_rating = Rating.objects.filter(
        content_type=content_type,
        object_id=obj.id
    ).aggregate(models.Avg('score'))['score__avg'] or 0

    return {
        'obj': obj,
        'content_type': content_type,
        'user_rating': user_rating or 0,
        'avg_rating': round(avg_rating, 1)
    }

@register.filter
def lte(value, arg):
    return value >= arg