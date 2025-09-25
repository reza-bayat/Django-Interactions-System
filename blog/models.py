from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    likes = GenericRelation('interactions.Like')
    bookmarks = GenericRelation('interactions.Bookmark')
    ratings = GenericRelation('interactions.Rating')    
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['title']

    def __str__(self):
        return self.title
