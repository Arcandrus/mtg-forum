from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.db import models
from django_summernote.fields import SummernoteTextField
from users.models import CustomUser

# Create your models here.
CATEGORY = ((0, "Deck Techs"),(1, "Combos & Strategy"),(2, "Rules & Card Help"),(3, "Looking for Games"), (4, "Social & Trading"))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    category = models.IntegerField(choices=CATEGORY, default=0)
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes')
    is_favourite = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.title} | written by {self.author}"
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"