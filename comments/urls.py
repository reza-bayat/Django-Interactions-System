from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/<int:content_type_id>/<int:object_id>/', views.CommentCreateView.as_view(), name='create'),
]