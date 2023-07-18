from django.contrib import admin
from .models import User, Post, Following

# Register models
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)