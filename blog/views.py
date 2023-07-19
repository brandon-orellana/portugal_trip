from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import Count
from . import models

class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        if 'pk' in self.kwargs:
            return queryset

        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')
class HomeView(TemplateView):
    """
    The Blog homepage.
    """
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the HomeView.
        Adds the most recent published posts to the context.
        """
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.published()\
                      .order_by('-published')[:10]
        context.update({'latest_posts': latest_posts})
        return context

class AboutView(TemplateView):
    """
    The Blog about page.
    """
    template_name = 'blog/about.html'

class TopicDetailView(DetailView):
    """
    A view that displays a single topic and its related posts.
    """
    model = models.Topic
    def get_queryset(self):
        """
        Returns the queryset for the TopicDetailView.
        Filters the queryset to only include the topic with the given slug.
        """
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Returns the context data for the TopicDetailView.
        Adds the topic's related posts to the context.
        """
        context = super().get_context_data(**kwargs)
        topic = self.get_object()
        topic_posts = models.Post.objects.published().filter(topics=topic)\
                      .order_by('-published')
        context.update({'topic_posts': topic_posts})
        return context

class TopicListView(ListView):
    model = models.Topic
    context_objects_name = 'topics'
    queryset = models.Post.objects.published().get_topics().order_by('name')

def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')