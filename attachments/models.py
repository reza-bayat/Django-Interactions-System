import os
import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = settings.AUTH_USER_MODEL

def validate_file_extension(value):
    allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.zip']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'پسوند {ext} مجاز نیست. پسوندهای مجاز: {", ".join(allowed_extensions)}')

def attachment_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    safe_name = f"{uuid.uuid4().hex}{ext}"
    return f'attachments/{instance.content_type.app_label}/{instance.content_type.model}/{instance.object_id}/{safe_name}'

class Attachment(models.Model):
    file = models.FileField(upload_to=attachment_upload_to,validators=[validate_file_extension])
    name = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.name or self.file.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        return self.file.name.split('.')[-1].lower() if '.' in self.file.name else ''

    @property
    def is_image(self):
        return self.file_extension in ['jpg', 'jpeg', 'png', 'gif', 'webp']