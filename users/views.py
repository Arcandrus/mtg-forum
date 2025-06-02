from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from posts.models import Post

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