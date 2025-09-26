# attachments/admin.py
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Attachment

class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1
    fields = ('file', 'name', 'uploaded_by', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('uploaded_by',)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_link', 'content_object', 'uploaded_by', 'created_at')
    list_filter = ('created_at', 'content_type')
    search_fields = ('name', 'uploaded_by__username')
    readonly_fields = ('content_type', 'object_id', 'created_at')
    autocomplete_fields = ('uploaded_by',)

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">مشاهده</a>'
        return "—"
    file_link.short_description = "فایل"
    file_link.allow_tags = True  # در Django قدیمی‌تر
    # در Django 5+ از `format_html` استفاده کنید:
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">مشاهده</a>', obj.file.url)
        return "—"