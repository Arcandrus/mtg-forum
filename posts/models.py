from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db import models
from django_summernote.fields import SummernoteTextField
from datetime import timedelta
from users.models import CustomUser
from django.conf import settings

# Create your models here.

class Post(models.Model):
    """
    Model representing a forum post with categories, author, content,
    likes, favourites, and timestamps. Supports tracking likes and comments count,
    and provides utility methods for display and URLs.
    """
    CATEGORY = (
        (0, "Deck Techs"),
        (1, "Combos & Strategy"),
        (2, "Rules & Card Help"),
        (3, "Looking for Games"), 
        (4, "Social & Trading")
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE
    )
    category = models.IntegerField(choices=CATEGORY, default=0)
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes')
    favourites = models.ManyToManyField(CustomUser, related_name='favourite_posts', blank=True)
    is_popular = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    @property
    def is_edited(self):
        """Returns True if the post has been updated after creation."""
        return (self.updated_on - self.created_on) > timedelta(seconds=1)
    
    @property
    def total_likes(self):
        """Returns the total number of likes for the post."""
        return self.likes.count()
    
    @property
    def comment_count(self):
        """Returns the total number of comments associated with the post."""
        return self.comments.count()

    def __str__(self):
        """Returns a string representation of the post."""
        return f"{self.title} | written by {self.author}"
    
    def get_absolute_url(self):
        """Returns the URL to access a detail view of this post."""
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def get_category_display_name(self):
        """Returns the display name of the category."""
        return dict(self.CATEGORY).get(self.category)

class Comment(models.Model):
    """
    Model representing a comment on a Post, including support for threaded replies
    via a self-referential foreign key to a parent comment.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        """Returns a string representation of the comment."""
        return f"Comment by {self.author} on {self.post}"