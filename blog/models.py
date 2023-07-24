"""
Contains the models used in the Django project.
"""

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

#Query Set
class PostQuerySet(models.QuerySet):
    """
    Custom Query Set
    """
    def published(self):
        """Published posts."""
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """Draft Posts"""
        return self.filter(status=self.model.DRAFT)

    #This is used to only provide topics that are used in atleast one post.
    def get_topics(self):
        """Topics of Posts"""
        return Topic.objects.filter(blog_posts__in=self).distinct()

    #This is used to get the authors in the queryset.
    def get_authors(self):
        User = get_user_model()
        return User.objects.filter(blog_posts__in=self).distinct()

#Topics Model
class Topic(models.Model):
    """
    Represents a topic
    """
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        """
        String for topic.
        """
        return self.name

    class Meta:
        """
        Ordering sequence.
        """
        ordering = ['name']

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('topic-detail', kwargs=kwargs)

#Post Model

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    objects = PostQuerySet.as_manager()

    title = models.CharField(max_length=255)

    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )

    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    #To timestamp when post becomes published status
    def publish(self):
        """Publishes this post."""
        self.status = self.PUBLISHED
        self.published = timezone.now()
        self.save()

    #To remove published status and timestamp (if applicable)
    def draft(self):
        """Removes published status and timestamp (if applicable)."""
        self.status = self.DRAFT
        self.published = None
        self.save()

    class Meta:
        """
        Sets the ordering sequence.
        """
        ordering = ['-created']

    def __str__(self):
        """
        String for post.
        """
        return self.title

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}
        return reverse('post-detail', kwargs=kwargs)

    content = RichTextUploadingField()

class Comment(models.Model):
    """
    Represents a comment
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    text = models.TextField(max_length=255)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def approve(self):
        """
        Approve comment.post
        """
        self.approved = True
        self.save()

    def __str__(self):
        """
        String for comments.
        """
        return self.text

    class Meta:
        """
        Ordering sequence
        """
        ordering = ['-created']

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'

class PhotoContestSubmission(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo = models.ImageField(
        blank=True,
        null=True,
        help_text='A photo submission for the contest.'
    )
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return ""