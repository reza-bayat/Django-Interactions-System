from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count, Avg

from .models import Like, Bookmark, Rating


class InteractionStatsMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            like_count=Count('likes', distinct=True),
            bookmark_count=Count('bookmarks', distinct=True),
            avg_rating=Avg('ratings__score')
        )

    def like_count_display(self, obj):
        return obj.like_count or 0
    like_count_display.short_description = 'لایک'
    like_count_display.admin_order_field = 'like_count'

    def bookmark_count_display(self, obj):
        return obj.bookmark_count or 0
    bookmark_count_display.short_description = 'بوکمارک'
    bookmark_count_display.admin_order_field = 'bookmark_count'

    def avg_rating_display(self, obj):
        avg = getattr(obj, 'avg_rating', None)
        if avg is not None:
            try:
                return f"{float(avg):.1f}"
            except (ValueError, TypeError):
                pass
        return "—"
    avg_rating_display.short_description = 'امتیاز'
    avg_rating_display.admin_order_field = 'avg_rating'


# === Inlines ===
class LikeInline(GenericTabularInline):
    model = Like
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = True
    verbose_name = "لایک"
    verbose_name_plural = "لایک‌ها"

class BookmarkInline(GenericTabularInline):
    model = Bookmark
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = True
    verbose_name = "بوکمارک"
    verbose_name_plural = "بوکمارک‌ها"

class RatingInline(GenericTabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'score', 'created_at')
    can_delete = True
    verbose_name = "امتیاز"
    verbose_name_plural = "امتیازها"