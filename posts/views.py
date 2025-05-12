from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponse
from .models import Post
# Create your views here.

def test(request):
    return HttpResponse("Hello, this is a plain text response.")

class PostList(generic.ListView):
    model = Post
    template_name = "posts/index.html"
    paginate_by = 6