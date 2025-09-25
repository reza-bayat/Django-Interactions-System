from django.views import View
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db import transaction
from .models import Like, Bookmark, Rating
from .forms import RatingForm

@method_decorator(login_required, name='dispatch')
class ToggleLikeView(View):
    def post(self, request, *args, **kwargs):
        content_type_id = kwargs['content_type_id']
        object_id = kwargs['object_id']
        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        with transaction.atomic():
            like, created = Like.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=object_id
            )
            if not created:
                like.delete()
                liked = False
                msg = "لایک شما حذف شد."
            else:
                liked = True
                msg = "با موفقیت لایک شد!"

        if request.htmx:
            html = render_to_string('interactions/like_button.html', {
                'obj': obj,
                'content_type': content_type,
                'liked': liked,
                'like_count': Like.objects.filter(content_type=content_type, object_id=object_id).count()
            },
            request=request
            )
            return HttpResponse(html)
        return JsonResponse({'liked': liked, 'message': msg})

@method_decorator(login_required, name='dispatch')
class ToggleBookmarkView(View):
    def post(self, request, *args, **kwargs):
        content_type_id = kwargs['content_type_id']
        object_id = kwargs['object_id']
        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        with transaction.atomic():
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=object_id
            )
            if not created:
                bookmark.delete()
                bookmarked = False
                msg = "بوکمارک حذف شد."
            else:
                bookmarked = True
                msg = "به بوکمارک‌ها اضافه شد!"

        if request.htmx:
            html = render_to_string('interactions/bookmark_button.html', {
                'obj': obj,
                'content_type': content_type,
                'bookmarked': bookmarked,
            },request=request)
            return HttpResponse(html)
        return JsonResponse({'bookmarked': bookmarked, 'message': msg})

@method_decorator(login_required, name='dispatch')
class RatingView(View):
    def post(self, request, *args, **kwargs):
        content_type_id = kwargs['content_type_id']
        object_id = kwargs['object_id']
        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        form = RatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            Rating.objects.update_or_create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                defaults={'score': score}
            )
            avg_rating = Rating.objects.filter(
                content_type=content_type,
                object_id=object_id
            ).aggregate(models.Avg('score'))['score__avg'] or 0

            if request.htmx:
                html = render_to_string('interactions/rating_widget.html', {
                    'obj': obj,
                    'content_type': content_type,
                    'user_rating': score,
                    'avg_rating': round(avg_rating, 1),
                },request=request)
                return HttpResponse(html)
            return JsonResponse({'success': True, 'avg_rating': avg_rating})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)