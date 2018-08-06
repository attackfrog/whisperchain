from django.shortcuts import render
from django.http import HttpResponseRedirect #, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

from .forms import LoginForm, SignupForm

def index(request):
    return render(request, "web/welcome.html")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.add_message(request, messages.WARNING, "The username and/or password you entered was invalid.")
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.add_message(request, messages.WARNING, "Please provide both a username and a password.")
            return HttpResponseRedirect(reverse("login"))
    
    else:
        return render(request, "web/login.html", {"form": LoginForm()})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "You successfully logged out.")
    return HttpResponseRedirect(reverse("index"))

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if not request.POST["password"] == request.POST["passconfirm"]:
                messages.add_message(request, messages.WARNING, "Your passwords didn't match.")
                form = SignupForm({
                    "username": request.POST["username"],
                    "email": request.POST["email"]
                    })
                return render(request, "web/signup.html", {"form": form})
            else:
                try:
                    user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
                    user.save()
                except IntegrityError:
                    messages.add_message(request, messages.WARNING, "That username is already taken.")
                    return HttpResponseRedirect(reverse("signup"))
                
                login(request, user)
                messages.add_message(request, messages.SUCCESS, f"You successfully created your account. Welcome to Whisperchain, {request.POST['username']}!")
                return HttpResponseRedirect(reverse("index"))

        else:
            messages.add_message(request, messages.WARNING, "Please fill out all of the fields.")
            return render(request, "web/signup.html", {"form": form})

    else:
        form = SignupForm()
        return render(request, "web/signup.html", {"form": form})
