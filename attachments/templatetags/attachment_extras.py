# attachments/templatetags/attachment_extras.py
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Attachment

register = template.Library()

@register.inclusion_tag('attachments/attachment_list.html')
def attachment_section(obj):
    content_type = ContentType.objects.get_for_model(obj)
    attachments = Attachment.objects.filter(
        content_type=content_type,
        object_id=obj.id
    ).order_by('-created_at')
    return {'attachments': attachments}