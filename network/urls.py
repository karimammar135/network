
from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    
    # React path
    path("index/<str:page>", views.index, name="index"),
    
    # Posts API
    path("posts", views.posts, name="posts"),
    path("editpost/<int:post_id>", views.editContent, name="editContent"),
    path("likepost/<int:post_id>", views.likePost, name="likePost"),
    path("followings/<str:current_user>/<str:profile_user>", views.followings, name="followings"),
    path("followings_page", views.followings_page, name="followings_page")
]
