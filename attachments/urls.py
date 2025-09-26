from django.urls import path
from . import views

app_name = 'attachments'

urlpatterns = [
    path('upload/<int:content_type_id>/<int:object_id>/', views.AttachmentUploadView.as_view(), name='upload'),
    path('delete/<int:pk>/', views.AttachmentDeleteView.as_view(), name='delete'),
    path('download/<int:attachment_id>/', views.SecureDownloadView.as_view(), name='download'),
]