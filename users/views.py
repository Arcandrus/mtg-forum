from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from posts.models import Post, Comment

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})

User = get_user_model()

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    context = {
        'profile_user': profile_user,
    }
    return render(request, 'users/profile.html', context)

def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'users/user_posts.html', {'profile_user': user, 'posts': posts})

def user_commented_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(comments__author=user).distinct()
    return render(request, 'users/user_commented_posts.html', {'profile_user': user, 'posts': posts})

@login_required
def user_settings(request):
    return render(request, 'users/settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user

        # Remove user from all likes on posts
        for post in Post.objects.filter(likes=user):
            post.likes.remove(user)

        # Delete comments by user
        Comment.objects.filter(author=user).delete()

        # Delete posts by user
        Post.objects.filter(author=user).delete()

        logout(request)
        user.delete()
        return redirect('account_logout')

    return render(request, 'users/account_delete_confirm.html')