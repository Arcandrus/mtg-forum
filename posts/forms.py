from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for creating and editing Post instances.
    Includes fields for title, category, and content.
    Uses Summernote rich text editor widget for the content field.
    """
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            'category': 'Select a Category',
        }

class CommentForm(forms.ModelForm):
    """
    Form for creating and editing Comment instances.
    Includes fields for comment content and optional parent comment for threaded replies.
    Uses Summernote widget for content and hides the parent field in the form.
    """
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': SummernoteWidget(),
            'parent': forms.HiddenInput(),
        }
