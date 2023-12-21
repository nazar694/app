from django.shortcuts import render, redirect
from .models import UserProfile, Message
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, HttpResponseServerError, JsonResponse


def index(request):
    return render(request, "pages/index.html", {"user": request.user})


def about(request):
    return render(request, "pages/about.html", {"user": request.user})


@csrf_exempt
def login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
    else:
        user = request.user
    if user is None or user.is_anonymous:
        return render(request, "account/login.html", {})
    else:
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/user/' + str(user.username))


@login_required
def user_page(request, username):
    user_profile = UserProfile.objects.get(user=User.objects.get(username=username))
    messages = Message.objects.all()
    user_list = UserProfile.objects.all()
    if user_profile:
        return render(request, "account/user.html", context={"user": user_profile, 'messages': messages, "user_list": user_list})
    else:
        return redirect('/login/')


def logout(request, username=None):
    auth_logout(request)
    return redirect('/login/')


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username).exists():
            return redirect('/login/')
        else:
            if username and password:
                User.objects.create_user(email=email, password=password, username=username, first_name=first_name, last_name=last_name)
                user_profile = UserProfile(user=User.objects.get(username=username))
                user_profile.save()
                auth_login(request, user_profile.user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/user/' + str(user_profile.user.username))
            else:
                return redirect('/signup/')
    return render(request, "account/signup.html", {})


def send_message(request):
    try:
        if request.method == 'POST':
            sender = request.user.username
            recipient = request.POST.get('recipient')
            content = request.POST.get('content')
            message = Message.objects.create(sender=sender, content=content, recipient=recipient)
            return JsonResponse({'sender': message.sender, 'recipient': message.recipient, 'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')})
        return JsonResponse({}, status=400)
    except Exception as e:
        return HttpResponseServerError(str(e))
