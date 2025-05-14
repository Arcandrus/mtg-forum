from . import views
from django.urls import path
from .views import PostList

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
]