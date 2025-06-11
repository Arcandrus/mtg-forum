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
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, F, Value, IntegerField
from .forms import PostForm, CommentForm
from .models import Post, Comment
# Create your views here.


class PostList(generic.ListView):
    """
    Display a paginated list of all posts on the site.
    Uses the 'posts/index.html' template and shows 6 posts per page.
    """
    model = Post
    template_name = "posts/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display a detailed view of a single post identified by its slug.
    Handles displaying top-level comments and processing new comment submissions.
    """
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
    """
    Toggle like status for the current user on the specified post.
    Supports AJAX requests by returning JSON with updated like info,
    otherwise redirects back to the post detail page.
    """
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
    """
    Generate a unique slug for a post based on its title.
    Appends a counter suffix if the slug already exists.
    """
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
    """
    Display a form to create a new post.
    On POST, validates and saves the post with the current user as author,
    generates a unique slug, and creates an excerpt from content.
    Provides success or error messages accordingly.
    """
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
    """
    Handle submission of a comment on a post.
    If POST and form is valid, save comment with author and post linked.
    Otherwise, display the post detail page with comment form and top-level comments.
    """
    post = get_object_or_404(Post, slug=slug)
    top_level_comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
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
    """
    Allow the author of a post to edit its content via a form.
    Handles POST submissions to update the post and returns JSON response with
    success status and updated content. On GET, renders the edit form HTML.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
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
    """
    Allow the author to delete their post and its comments.
    Handles POST to delete and redirects to post list.
    GET requests render a confirmation page.
    Unauthorized users are redirected with an error message.
    """
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
    """
    Allow the author of a comment to edit its content via a form.
    Handles POST submissions to update the comment and returns JSON response with
    success status and updated content. On GET, renders the edit form HTML.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

            # Return JSON response like your post_edit view
            return JsonResponse({
                'success': True,
                'updated_content': comment.content,
                'updated_on': django_date_format(localtime(comment.updated_on), 'N j, Y, P') if hasattr(comment, 'updated_on') else ''
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = CommentForm(instance=comment)
        html = render_to_string('posts/edit_comment.html', {
            'form': form,
            'comment': comment,
        }, request=request)
        return HttpResponse(html)


@login_required
def delete_comment(request, comment_id):
    """
    Allow the author of a comment to delete it.
    Handles POST to delete the comment and redirects to the post detail.
    GET requests render a confirmation page.
    Unauthorized users are redirected with an error message.
    """
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
    """
    Display posts filtered by a specific category.
    If the category name is valid, fetch posts for that category, paginate,
    and render the categories template. Otherwise, show 'Unknown Category'.
    """
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
    """
    Toggle the favourite status of a post for the current user.
    Only accepts AJAX POST requests.
    Returns JSON with updated favourite status and count.
    """
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

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def favourite_posts(request):
    """
    Display a paginated list of the current user's favourite posts,
    ordered by creation date descending.
    """
    posts = request.user.favourite_posts.all().order_by('-created_on')
    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/favourite_posts.html', {
        'page_obj': page_obj
    })


def popular_posts(request):
    """
    Display posts sorted by popularity within a selected time period.
    Popularity is based on the sum of likes and comments counts.
    Supports filtering by periods: '24h' (default), '7d', '30d', and 'all'.
    Results are paginated.
    """
    period = request.GET.get('period', '24h')
    now = timezone.now()

    if period == '7d':
        since = now - timedelta(days=7)
    elif period == '30d':
        since = now - timedelta(days=30)
    elif period == 'all':
        since = None
    else:
        since = now - timedelta(days=1)

    if since:
        posts = Post.objects.filter(created_on__gte=since)
    else:
        posts = Post.objects.all()

    posts = posts.annotate(
        likes_count=Coalesce(Count('likes'), Value(0), output_field=IntegerField()),
        comments_count=Coalesce(Count('comments'), Value(0), output_field=IntegerField())
    ).annotate(
        total_activity=F('likes_count') + F('comments_count')
    ).order_by('-total_activity')

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/popular.html', {
        'page_obj': page_obj,
        'period': period
    })


def search_results(request):
    """
    Perform a search for posts matching the query string in title, content,
    or author's username. Displays paginated results.
    """
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
