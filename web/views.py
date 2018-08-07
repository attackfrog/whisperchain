from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from hashlib import blake2b
from datetime import datetime

from .models import Chain, Picture, Phrase, CHAIN_CODE_LENGTH
from .forms import LoginForm, SignupForm, ChainCodeForm, NewChainForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, "web/welcome.html")
    else:
        context = {
            "form": ChainCodeForm(),
            "user_chains": Chain.objects.filter(users__username=request.user.username), # pylint: disable=no-member
            "public_chains": Chain.objects.filter(isPublic=True).filter(isOpen=True) # pylint: disable=no-member
        }
        return render(request, "web/main.html", context)


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
                return render(request, "web/login.html", {"form": form})
        else:
            return render(request, "web/login.html", {"form": form})
    
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
            user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"You successfully created your account. Welcome to Whisperchain, {request.POST['username']}!")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "web/signup.html", {"form": form})

    else:
        return render(request, "web/signup.html", {"form": SignupForm()})


def profile(request):
    return HttpResponse("User profile goes here.")


def chain(request, code):
    if not len(code) == 6 or not code.isalnum():
        return HttpResponse(f"{code} is not a valid code.")
    
    try:
        chain = Chain.objects.get(code=code) # pylint: disable=no-member
    except Chain.DoesNotExist: # pylint: disable=no-member
        return HttpResponse(f"There is no chain that with the code {code}.")

    return HttpResponse(f"Chain display goes here. Code was {code}.")


def create(request):
    if request.method == "POST":
        form = NewChainForm(request.POST)
        if form.is_valid():
            name = request.POST["name"]
            maxUsers = request.POST["maxUsers"]
            isPublic = "isPublic" in request.POST and request.POST["isPublic"] == "on"
            code = blake2b(str.encode(name + datetime.now().isoformat()), digest_size=int(CHAIN_CODE_LENGTH/2)).hexdigest() # pylint: disable=unexpected-keyword-arg
            chain = Chain(name=name, code=code, maxUsers=maxUsers, isPublic=isPublic)
            chain.save()
            return HttpResponseRedirect(f"chain/{code}")

        else:
            return render(request, "web/create.html", {"form": form})

    else:
        return render(request, "web/create.html", {"form": NewChainForm()})
    