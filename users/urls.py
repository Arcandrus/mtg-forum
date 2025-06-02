from django.urls import path
from . import views
from .views import update_profile

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', update_profile, name='update_profile'),
]