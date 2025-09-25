from django.urls import path

from . import views


app_name = 'interactions'

urlpatterns = [
    path('like/<int:content_type_id>/<int:object_id>/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('bookmark/<int:content_type_id>/<int:object_id>/', views.ToggleBookmarkView.as_view(), name='toggle_bookmark'),
    path('rate/<int:content_type_id>/<int:object_id>/', views.RatingView.as_view(), name='rate_object'),
]

