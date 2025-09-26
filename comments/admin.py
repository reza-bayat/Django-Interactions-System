from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ("id", "user", "short_content", "content_object", "approved", "created_at")
    list_filter = ("approved", "created_at", "content_type")
    search_fields = ("content", "user__username", "user__email")
    raw_id_fields = ("user",)
    mptt_level_indent = 20
    actions = ["approve_comments", "disapprove_comments"]

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = "متن"

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} نظر تأیید شد.")
    approve_comments.short_description = "تأیید نظرات انتخاب‌شده"

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"{updated} نظر رد شد.")
    disapprove_comments.short_description = "رد نظرات انتخاب‌شده"
