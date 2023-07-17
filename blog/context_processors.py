from django.db.models import Count
from . import models

def base_context(request):
    topics = models.Post.objects.published().get_topics()\
        .annotate(blog_count=Count('blog_posts'))\
        .order_by('-blog_count')

    authors = models.Post.objects.published().get_authors()\
             .order_by('first_name')

    return {'topics': topics, 'authors': authors}