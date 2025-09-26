from django.urls import path

from . import views


urlpatterns = [
    path('', views.BlogView.as_view(), name='blog-view'),
    path('<int:pk>', views.PostDetailView.as_view(), name='blog-detail-view'),
]

