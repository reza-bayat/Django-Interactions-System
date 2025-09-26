from django.shortcuts import render
from django.views import generic
from django.contrib.contenttypes.models import ContentType

from blog.models import Post


class BlogView(generic.ListView):
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = ContentType.objects.get_for_model(self.object)
        return context