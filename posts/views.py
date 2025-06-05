from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.dateformat import format as django_date_format
from django.contrib import messages
from datetime import timedelta
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, F
from .forms import PostForm, CommentForm
from .models import Post, Comment
# Create your views here.

class PostList(generic.ListView):
    model = Post
    template_name = "posts/index.html"
    paginate_by = 6

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = form.cleaned_data.get('parent')
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form,
    })

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
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'There was an error in your form. Please fix the issues below.')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    top_level_comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # DEBUG: If parent is missing here, this is the problem
            if not comment.parent:
                messages("Parent not assigned in form.cleaned_data!")

            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'form': form,
        'comments': top_level_comments,
    })

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # Update excerpt: first 200 words of content
            post.excerpt = ' '.join(post.content.split()[:200])
            post.save()
            
            updated_time = django_date_format(localtime(post.updated_on), 'N j, Y, P')
            return JsonResponse({
                'success': True,
                'updated_content': post.content,
                'updated_on': updated_time,
            })
        return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = PostForm(instance=post)
        html = render_to_string('posts/edit_post.html', {
            'form': form,
            'post': post,
        }, request=request)
        return HttpResponse(html)
    
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_detail', slug=slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post and its comments were deleted successfully.")
        return redirect('post_list')
    
    return render(request, 'posts/confirm_delete.html', {'post': post})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('post_detail', slug=comment.post.slug)

    return HttpResponseNotAllowed(['POST'])

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('post_detail', slug=comment.post.slug)

    if request.method == "POST":
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', slug=post_slug)

    return render(request, 'posts/confirm_delete_comment.html', {'comment': comment})

CATEGORY_CHOICES = dict(Post.CATEGORY)
CATEGORY_SLUGS = {slugify(name): id for id, name in CATEGORY_CHOICES.items()}

def category_posts(request, category_name=None):
    categories = CATEGORY_CHOICES 

    if category_name in CATEGORY_SLUGS:
        category_id = CATEGORY_SLUGS[category_name]
        posts = Post.objects.filter(category=category_id)
        pretty_category_name = CATEGORY_CHOICES[category_id]
        selected_category = category_name
    else:
        posts = Post.objects.none()
        pretty_category_name = "Unknown Category"
        selected_category = None

    paginator = Paginator(posts, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'posts': page_obj, 
        'page_obj': page_obj,
        'selected_category': selected_category,
        'category_name': pretty_category_name,
    }
    return render(request, 'posts/categories.html', context)

@require_POST
@login_required
def toggle_favourite(request, slug):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = get_object_or_404(Post, slug=slug)
        user = request.user
        favourited = False

        if post.favourites.filter(id=user.id).exists():
            post.favourites.remove(user)
        else:
            post.favourites.add(user)
            favourited = True

        return JsonResponse({
            'favourited': favourited,
            'total_favourites': post.favourites.count()
        })

    # Fallback if not an AJAX request — optional
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def favourite_posts(request):
    posts = request.user.favourite_posts.all().order_by('-created_on')
    paginator = Paginator(posts, 4)  # 6 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/favourite_posts.html', {
        'page_obj': page_obj
    })

def popular_posts(request):
    period = request.GET.get('period', '24h')
    now = timezone.now()

    if period == '7d':
        since = now - timedelta(days=7)
    elif period == '30d':
        since = now - timedelta(days=30)
    elif period == 'all':
        since = None
    else:  # default to last 24 hours
        since = now - timedelta(days=1)

    if since:
        posts = Post.objects.filter(created_on__gte=since)
    else:
        posts = Post.objects.all()

    posts = posts.annotate(
        total_activity=F('likes') + F('comments')
    ).order_by('-total_activity')

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/popular.html', {
        'page_obj': page_obj,
        'period': period
    })

def search_results(request):
    query = request.GET.get('q', '')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }

    return render(request, 'posts/search_results.html', context)