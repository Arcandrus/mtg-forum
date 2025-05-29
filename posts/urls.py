from . import views
from django.urls import path
from .views import PostList

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
]