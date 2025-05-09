from . import views
from django.urls import path
from .views import test

urlpatterns = [
    path('posts/', test)
]