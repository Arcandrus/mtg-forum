from . import views
from django.urls import path
from .views import PostList

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('search/', views.search_results, name='search_results'),
    path("posts/categories/", views.category_posts, name="category_list"),
    path("posts/categories/<str:category_name>/", views.category_posts, name="category_posts_filtered"),
    path('popular/', views.popular_posts, name='popular_posts'),
    path('post/<slug:slug>/favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/', views.favourite_posts, name='favourite_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]