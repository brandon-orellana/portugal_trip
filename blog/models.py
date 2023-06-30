"""
Contains the models used in the Django project.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone

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

    title = models.CharField(max_length=255)
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
