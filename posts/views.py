from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import JsonResponse
from django.contrib import messages
from .forms import PostForm
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

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes
        })

    return redirect('post_detail', slug=slug)

def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    from .models import Post
    while Post.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = generate_unique_slug(post.title)
            post.excerpt = ' '.join(post.content.split()[:200])
            post.save()
            messages.success(request, 'Your post was created successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'There was an error in your form. Please fix the issues below.')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})