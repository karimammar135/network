from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Like, Following

# Landing page
def landing_page(request):
    if request.user.is_authenticated:
        # Return main page
        return redirect(reverse("index", kwargs={'page':'allposts_page'}))

    else:
        # Return animated Login page
        return render(request, "network/login.html", {
            "animated": True
        })

# REACT Index ROUTE
def index(request, page):
    return render(request, "index.html", { 
        'current_user': request.user,
        'is_authenticated': request.user.is_authenticated
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
            return HttpResponseRedirect(reverse("index", kwargs={'page':'allposts_page'}))
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
    return HttpResponseRedirect(reverse("index", kwargs={'page':'allposts_page'}))


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
        return HttpResponseRedirect(reverse("index", kwargs={'page':'allposts_page'}))
    else:
        return render(request, "network/register.html")


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

        return redirect(reverse("index", kwargs={'page':'allposts_page'}))


''' Posts API '''

# Posts data API
def posts(request):

    # GET METHOD
    if request.method == "GET":
        usernames = json.loads(request.GET.get("postsfor"))
        if usernames[0] == "all":
            # Get 10 posts(if exists) from the database
            posts = Post.objects.all().order_by('-created_on')
            
        else:
            authors = User.objects.filter(username__in=usernames)
            posts = Post.objects.filter(author__in=authors).order_by('-created_on')

        paginator = Paginator(posts, 10)
        page_num = int(request.GET.get("page_num"))
        page_obj = paginator.get_page(page_num)

        return JsonResponse([[post.serialize() for post in page_obj], [{'has_previous': page_obj.has_previous(), 'has_next': page_obj.has_next()}]], safe=False)
    
    # POST method
    elif request.method == "POST":
        data = json.loads(request.body)
        if data["content"] == "":
            return JsonResponse({"error": "Write something in the texarea."}, status=400)
        else:
            author = request.user
            content = data["content"]
            # Save data in the database
            post = Post(author=author, content=content)
            post.save()

            return JsonResponse({"message": "Post submitted successfully."}, status=201)
    
    else:
        return JsonResponse({"error": "Unsupported request method."}, status=400)
    

# Edit post content API
def editContent(request, post_id):
    # Get the post
    try:
        post = Post.objects.get(author=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # PUT METHOD (edit content of the post)
    if request.method == "PUT":
        data = json.loads(request.body)
        # Save the new content to the database
        post.content = data["content"]
        post.save()

        return JsonResponse({"message": "Edited successfully."}, status=201)

    else:
        return JsonResponse({"error": "PUT oe Get request required."}, status=400)
    
# Likes API
def likePost(request, post_id):
    # Get the post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # GET method
    if request.method == "GET":
        # get the likes of the post
        likes = post.likes.all()

        # Return likes in json format
        return JsonResponse([like.serialize() for like in likes], safe=False)
    
    # POST method
    elif request.method == "POST":
        # Get the submitted data
        data = json.loads(request.body)
        # Like the post
        if data['action'] == 'like':
            like = Like(user=request.user, post=post)
            like.save()
            return JsonResponse({"message": "liked"}, status=201)

        # unlike the post
        else:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return JsonResponse({"message": "unliked"}, status=201)
    
    else:
        return JsonResponse({"error": "POST oe Get request required."}, status=400)


# following table API
def followings(request, current_user, profile_user):
    
    # POST method
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            follower = User.objects.get(username=data["follower"])
            following = User.objects.get(username=data["following"])
        except User.DoesNotExist:
            return JsonResponse({"error": "follower and/or following user doesn't exist"}, status=400)
            
        # Add data to the database
        if data["action"] == "+":
            try:
                Following.objects.get(following=following, follower=follower)
            except Following.DoesNotExist:
                follow = Following(following=following, follower=follower)
                follow.save()
            return JsonResponse({"message": "user successfully followed"}, status=201)
        else:
            try:
                follow = Following.objects.get(following=following, follower=follower)
            except Following.DoesNotExist:
                return JsonResponse({"error": "user not followed to be unfollowed"}, status=400)
            follow.delete()
            return JsonResponse({"message": "user successfully unfollowed"}, status=201)
    
    elif request.method == "GET":

        # Error checking
        if current_user == "AnonymousUser":
            return JsonResponse({"error": "Not signed in can't follow users"})
        # Collect data
        profile_user = User.objects.get(username=profile_user)
        follower = User.objects.get(username=current_user)

        # Get the followers and followings of the profile user
        followers = profile_user.followers.all()
        followings = profile_user.followings.all()

        # Checking if the current user has followed the profile user or not
        try:
            follow = Following.objects.get(follower=follower, following=profile_user)
        except Following.DoesNotExist:
            return JsonResponse([{"follow": "+"}, {"followers_num": len(followers), "followings_num": len(followings)}], safe=False)
        
        return JsonResponse([{"follow": "-"}, {"followers_num": len(followers), "followings_num": len(followings)}], safe=False)
    
# Followings Page
def followings_page(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Create followings list
        followings = []
        for following in current_user.followings.all():
            if following == "":
                return JsonResponse({"message": "user has no followers"}, status=201)
            
            followings.append(following.following.username)
        
        return JsonResponse({"followings": followings}, status=201)

    else:
        return JsonResponse({"message": "not auth"}, status=201)
