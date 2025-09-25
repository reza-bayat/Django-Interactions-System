from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType
from .models import Like, Bookmark, Rating




# === Mixin پایه ===
class InteractionBaseAdmin(admin.ModelAdmin):
    list_select_related = ('user', 'content_type')
    readonly_fields = ('user', 'content_type', 'object_id', 'content_object', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at', 'content_type')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False

    def content_object_display(self, obj):
        model_class = obj.content_type.model_class()
        if not model_class:
            return _("شیء حذف شده")
        try:
            content_object = model_class.objects.get(pk=obj.object_id)
        except model_class.DoesNotExist:
            return _("شیء حذف شده")
        
        display_text = str(content_object)
        
        # لینک به ادمین
        try:
            app_label = obj.content_type.app_label
            model = obj.content_type.model
            url = reverse(f"admin:{app_label}_{model}_change", args=[obj.object_id])
            return mark_safe(f'<a href="{url}">{display_text}</a>')
        except:
            return display_text
    content_object_display.short_description = _("محتوا")
    content_object_display.admin_order_field = 'object_id'

# === لایک‌ها ===
@admin.register(Like)
class LikeAdmin(InteractionBaseAdmin):
    list_display = ('user', 'content_object_display', 'content_type', 'created_at')
    list_display_links = ('user',)


# === بوکمارک‌ها ===
@admin.register(Bookmark)
class BookmarkAdmin(InteractionBaseAdmin):
    list_display = ('user', 'content_object_display', 'content_type', 'created_at')
    list_display_links = ('user',)


# === امتیازها ===
@admin.register(Rating)
class RatingAdmin(InteractionBaseAdmin):
    list_display = ('user', 'content_object_display', 'content_type', 'score', 'created_at')
    list_display_links = ('user',)
    list_filter = ('score', 'created_at', 'content_type')

