from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content_type_id = kwargs['content_type_id']
        object_id = kwargs['object_id']
        parent_id = request.POST.get('parent_id')

        content_type = get_object_or_404(ContentType, id=content_type_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            if parent_id:
                comment.parent_id = parent_id
            comment.save()

            # --- اگر پاسخ است ---
            if parent_id:
                return HttpResponse(f"""
                    <div class="bg-green-100 border border-green-400 text-green-700 px-3 py-2 rounded mb-2">
                    پاسخ شما ثبت شد و پس از تأیید نمایش داده می‌شود.
                    </div>
                    <script>
                        setTimeout(() => {{
                            const replySection = document.getElementById('reply-section-{parent_id}');
                            if(replySection) replySection.classList.add('hidden');
                        }}, 2000);  // بعد از 2 ثانیه فرم بسته می‌شود
                    </script>
                """)                
            # --- اگر کامنت ریشه است ---
            return HttpResponse(f"""
              <div class="bg-green-100 border border-green-400 text-green-700 px-3 py-2 rounded mb-3">
                نظر شما ثبت شد و پس از تأیید نمایش داده می‌شود.
              </div>
              <form hx-post="/comments/create/{content_type_id}/{object_id}/"
                    hx-swap="outerHTML"
                    hx-target="#comment-form-{object_id}"
                    class="htmx-form mt-3">
                {request.csrf_processing_done and ''}
                <textarea name="content" rows="3"
                          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                          placeholder="نظر خود را بنویسید..."></textarea>
                <div class="mt-2">
                  <button type="submit"
                          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    ارسال
                  </button>
                </div>
              </form>
            """)

        # --- اگر خطا بود ---
        errors = ''.join([f"<div>{e}</div>" for e in form.errors.values()])
        return HttpResponse(f"""
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-3">
              خطا: {errors}
            </div>
        """, status=400)