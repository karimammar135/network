
from django.urls import path

from . import views

urlpatterns = [
    path("", views.animation, name="animation"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("test", views.test, name="test"),
    path("create_post", views.create_post, name="create_post"),
    
    # Posts API
    path("posts", views.posts, name="posts")
]
