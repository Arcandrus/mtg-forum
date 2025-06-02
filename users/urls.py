from django.urls import path
from . import views
from .views import update_profile

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', update_profile, name='update_profile'),
    path('users/<str:username>/', views.profile_view, name='profile'),
    path('users/<str:username>/posts/', views.user_posts, name='user_posts'),
    path('users/<str:username>/commented/', views.user_commented_posts, name='user_commented_posts')
]