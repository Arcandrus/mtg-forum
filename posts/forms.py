from django import forms
from .models import Post, CATEGORY
from django_summernote.widgets import SummernoteWidget

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