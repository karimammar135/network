from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
import datetime

from .models import User, Post


def index(request):
    # Get all posts from the database
    posts_data = Post.objects.all().order_by('-created_on')

    # Put all posts in an array
    posts_list = []
    for post in posts_data:
        posts_list.append(post)
    
    # Make a list of posts' dictionaries
    posts = []
    for i in range(len(posts_list)):
        # Transform each post into a dict object
        post_dict = {}
        for el in vars((posts_list)[i]):
            if el == 'author_id':
                author = User.objects.get(id=(vars(posts_list[i])[el]))
                post_dict['author']  = str(author)

            elif el == 'created_on':
                creation_post = Post.objects.get(created_on=(vars(posts_list[i])[el]))
                date = str(creation_post.created_on)[:19]
                months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                month = int(date[6:7])
                month_name = months_in_year[month - 1]
                
                created_on = f"{month_name}, {date[8:10]}, {date[0:4]}, {datetime.datetime.strptime(date[11:16] ,'%H:%M').strftime('%I:%M %p')}"
                post_dict['created_on']  = str(created_on)
            else:
                post_dict[el] = str(vars(posts_list[i])[el])
        del post_dict['_state']
        # Add the dictionary into the posts list
        posts.append(json.dumps(post_dict))
    print(json.dumps(posts))

    return render(request, "network/index.html", {
        'posts': json.dumps(posts), 
        'current_user': request.user
    })

# Animated Login View
def animation(request):
    return render(request, "network/login.html", {
        "animated": True
    })

# Login view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "animated": False,
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html", {
            "animated": False
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# test
def test(request):
    return render(request, "network/test.html")

# Create New Post
def create_post(request):
    # Post method
    if request.method == "POST":
        # Collect submited data
        author = request.user
        content = request.POST['content']

        # Save the data into the POST model
        post = Post(author=author, content=content)
        post.save()

        return redirect(reverse("index"))



''' API '''

# Posts API
def posts(request):
    # Get all posts from the database
    posts_data = Post.objects.all().order_by('-created_on')

    # Put all posts in an array
    posts_list = []
    for post in posts_data:
        posts_list.append(post)
    
    # Make a list of posts' dictionaries
    posts = []
    for i in range(len(posts_list)):
        # Transform each post into a dict object
        post_dict = {}
        for el in vars((posts_list)[i]):
            if el == 'author_id':
                author = User.objects.get(id=(vars(posts_list[i])[el]))
                post_dict['author']  = str(author)

            elif el == 'created_on':
                creation_post = Post.objects.get(created_on=(vars(posts_list[i])[el]))
                date = str(creation_post.created_on)[:19]
                months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                month = int(date[6:7])
                month_name = months_in_year[month - 1]
                
                created_on = f"{month_name}, {date[8:10]}, {date[0:4]}, {datetime.datetime.strptime(date[11:16] ,'%H:%M').strftime('%I:%M %p')}"
                post_dict['created_on']  = str(created_on)
            else:
                post_dict[el] = str(vars(posts_list[i])[el])
        del post_dict['_state']
        # Add the dictionary into the posts list
        posts.append(post_dict)
    
    # GET METHOD
    if request.method == "GET":
        return JsonResponse([json.dumps(post) for post in posts], safe=False)
    