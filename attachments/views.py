import os
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from urllib.parse import quote

from .models import Attachment
from .forms import AttachmentForm

class AttachmentUploadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content_type_id = kwargs['content_type_id']
        object_id = kwargs['object_id']
        content_type = get_object_or_404(ContentType, id=content_type_id)
        obj = get_object_or_404(content_type.model_class(), id=object_id)

        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for f in files:
                Attachment.objects.create(
                    file=f,
                    uploaded_by=request.user,
                    content_type=content_type,
                    object_id=object_id
                )
            if request.htmx:
                html = render_to_string('attachments/partials/attachment_list.html', {
                    'attachments': Attachment.objects.filter(
                        content_type=content_type,
                        object_id=object_id
                    ),
                    'content_type': content_type,
                    'object_id': object_id,
                    'request': request
                }, request=request)
                return HttpResponse(html)
        return HttpResponse(status=400)

class AttachmentDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk, uploaded_by=request.user)
        attachment.delete()
        return HttpResponse(status=200)
    
    

@method_decorator(login_required, name='dispatch')
class SecureDownloadView(View):
    def get(self, request, attachment_id):
        attachment = get_object_or_404(Attachment, id=attachment_id)
        
        # بررسی دسترسی (اختیاری ولی توصیه می‌شود)
        # مثال: فقط اگر مقاله عمومی باشد یا کاربر مجاز باشد
        # content_obj = attachment.content_object
        # if not (request.user.is_staff or ...):
        #     raise Http404("دسترسی مجاز نیست.")

        file_path = attachment.file.path
        if not os.path.exists(file_path):
            raise Http404("فایل یافت نشد.")

        # استخراج نام اصلی فایل با پسوند
        original_filename = os.path.basename(attachment.file.name)

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            # تنظیم هدر برای دانلود با نام اصلی و پسوند صحیح
            # response['Content-Disposition'] = f'attachment; filename="{original_filename}"'
            safe_filename = quote(original_filename)
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}"; filename*=UTF-8\'\'{safe_filename}'        
            return response
        
        