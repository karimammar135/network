from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Author: {self.author}, Content: {self.content}, Created_on: {self.created_on}"
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "created_on": self.created_on.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"User:{self.user}, Post_id:{self.post.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post_id": self.post.id
        }

class Following(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')

    def __str__(self):
        return f"follower: {self.follower}, following: {self.following}"