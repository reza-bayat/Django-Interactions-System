from django.shortcuts import render
from django.views import generic

from blog.models import Post


class BlogView(generic.ListView):
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'
