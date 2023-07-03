from django.shortcuts import render
from django.db.models import Count
from . import models

def home(request):
    """
    The Blog homepage.
    """
    # Get last 10 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:10]
    topics = models.Post.objects.published().get_topics().annotate(blog_count=Count('blog_posts'))\
            .order_by('-blog_count')
    context = {
        'topics': topics,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/home.html', context)
