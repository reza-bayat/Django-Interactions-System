from django import template
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm
from ..models import Comment

register = template.Library()

@register.inclusion_tag("comments/comment_list.html", takes_context=True)
def comment_list(context, obj):
    request = context['request']
    content_type = ContentType.objects.get_for_model(obj)

    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=obj.id,
        parent=None,
        approved=True
    ).select_related("user").prefetch_related("children__user")

    return {
        "comments": comments,
        "content_type": content_type,
        "object_id": obj.id,
        "form": CommentForm(),
        "request": request,
    }
