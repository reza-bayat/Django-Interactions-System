# blog/admin.py
from django.contrib import admin
from interactions.admin_mixins import InteractionStatsMixin, LikeInline, BookmarkInline, RatingInline
from .models import Post

@admin.register(Post)
class PostAdmin(InteractionStatsMixin, admin.ModelAdmin):
    list_display = ('title', 'like_count_display', 'bookmark_count_display', 'avg_rating_display', 'created_at')
    list_filter = ('created_at',)
    inlines = [LikeInline, BookmarkInline, RatingInline]