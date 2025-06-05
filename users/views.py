from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from posts.models import Post, Comment

@login_required
def update_profile(request):
    """
    Allow logged-in users to update their profile information.
    On POST, validates and saves the updated data.
    On GET, displays the form pre-filled with current user data.
    Redirects to the user's profile page after a successful update.
    """
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
    """
    Display the profile page for a user identified by username.
    """
    profile_user = get_object_or_404(User, username=username)
    context = {
        'profile_user': profile_user,
    }
    return render(request, 'users/profile.html', context)

def user_posts(request, username):
    """
    Show all posts authored by the user with the given username.
    """
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'users/user_posts.html', {'profile_user': user, 'posts': posts})

def user_commented_posts(request, username):
    """
    Display all posts on which the user with the given username has commented.
    Only unique posts are shown.
    """
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(comments__author=user).distinct()
    return render(request, 'users/user_commented_posts.html', {'profile_user': user, 'posts': posts})

@login_required
def user_settings(request):
    """
    Render the user settings page for logged-in users.
    """
    return render(request, 'users/settings.html')

@login_required
def delete_account(request):
    """
    Allow logged-in users to delete their account.
    On POST:
    - Remove user's likes from all posts
    - Delete user's comments and posts
    - Log out the user and delete their user record
    Redirects to the logout page afterwards.
    On GET, renders a confirmation page.
    """
    if request.method == 'POST':
        user = request.user

        # Remove user from likes on posts
        for post in Post.objects.filter(likes=user):
            post.likes.remove(user)

        # Delete all comments by user
        Comment.objects.filter(author=user).delete()

        # Delete all posts by user
        Post.objects.filter(author=user).delete()

        logout(request)
        user.delete()
        return redirect('account_logout')

    return render(request, 'users/account_delete_confirm.html')