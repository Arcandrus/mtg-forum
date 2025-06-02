from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
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
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': SummernoteWidget(),
            'parent': forms.HiddenInput(),
        }