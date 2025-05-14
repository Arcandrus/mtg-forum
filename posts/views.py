from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Post
# Create your views here.

class PostList(generic.ListView):
    model = Post
    template_name = "posts/index.html"
    paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual :model:`posts.Post`.

    **Context**

    ``post``
        An instance of :model:`posts.Post`.

    **Template:**

    :template:`posts/post_detail.html`
    """

    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/post_detail.html', {'post': post})