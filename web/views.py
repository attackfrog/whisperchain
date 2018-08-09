from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Used for generating unique ID codes for chains
from hashlib import blake2b
from datetime import datetime

from .models import Chain, Picture, Phrase, CHAIN_CODE_LENGTH
from .forms import LoginForm, SignupForm, ChainCodeForm, NewChainForm, SubmitPhraseForm, SubmitPictureForm
from .helpers import nextPlayer


# Shows the home page to logged in users and a welcome page to logged out visitors
def index(request):
    if not request.user.is_authenticated:
        return render(request, "web/welcome.html")
    else:
        context = {
            "form": ChainCodeForm(),
            "user_chains": Chain.objects.filter(users__username=request.user.username).filter(isActive=True), # pylint: disable=no-member
            "public_chains": Chain.objects.filter(isPublic=True).filter(isOpen=True) # pylint: disable=no-member
        }
        return render(request, "web/main.html", context)


# Displays a login form and handles login requests
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        # Use basic form validation and render validation errors if they occur
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                # If user info wasn't a match, inform the user with a notification message
                messages.add_message(request, messages.ERROR, "The username and/or password you entered was invalid.")
                return render(request, "web/login.html", {"form": form})
        else:
            return render(request, "web/login.html", {"form": form})
    
    else:
        return render(request, "web/login.html", {"form": LoginForm()})


# Handles logout requests
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "You successfully logged out.")
    return HttpResponseRedirect(reverse("index"))


# Displays a signup form and handles new user account requests
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        # Validate using SignupForm's validation method, and pass any errors to the user. If there were none, create the account
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"You successfully created your account. Welcome to Whisperchain, {form.cleaned_data['username']}!")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "web/signup.html", {"form": form})

    else:
        return render(request, "web/signup.html", {"form": SignupForm()})


# Displays a user's profile
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    # If the specified username doesn't exist, notify the user with a message
    except User.DoesNotExist: # pylint: disable=no-member
        messages.add_message(request, messages.WARNING, f"There is no user by the username {username}.")
        return HttpResponseRedirect(reverse("index"))

    return render(request, "web/profile.html", {"user": user})


# Displays a "whisper chain", as specified by the chain's ID code
def chain(request, code):
    # Do some simple validation on the code
    if not len(code) == CHAIN_CODE_LENGTH or not code.isalnum():
        messages.add_message(request, messages.WARNING, f"{code} is not a valid code.")
        return HttpResponseRedirect(reverse("index"))
    
    # Get the specified chain from the database, if it exists
    try:
        chain = Chain.objects.get(code=code) # pylint: disable=no-member
    except Chain.DoesNotExist: # pylint: disable=no-member
        messages.add_message(request, messages.WARNING, f"There is no chain with the code {code}.")
        return HttpResponseRedirect(reverse("index"))

    # If the chain still needs more users to start, display the formingchain.html template
    if chain.isOpen:
        form = ChainCodeForm(initial={"code": code})
        in_chain = request.user in chain.users.all()
        chain_uri = request.build_absolute_uri(reverse("chain", kwargs={"code": code}))
        context = {
            "logged_in": request.user.is_authenticated,
            "chain": chain,
            "form": form,
            "in_chain": in_chain,
            "chain_uri": chain_uri
        }
        return render(request, "web/formingchain.html", context)

    # Otherwise, if the chain is full, display the chain.html template
    else:
        pictures = chain.pictures.all()
        phrases = chain.phrases.all()
        # Collate phrases and pictures to be displayed in the proper order in the template
        submissions = []
        for i in range(chain.currentPosition):
            if i % 2 == 0:
                submissions.append(phrases[int(i/2)])
            else:
                submissions.append(pictures[int(i/2)])

        # Provide the appropriate form, if it's the current user's turn to submit something
        active_user = nextPlayer(chain.currentPosition, chain.users.all())
        if active_user == request.user:
            if chain.currentPosition % 2 == 0:
                form = SubmitPhraseForm()
            else:
                form = SubmitPictureForm()
        else:
            form = False

        context = {
            "chain": chain,
            "submissions": submissions,
            "logged_in": request.user.is_authenticated,
            "form": form,
            "active_user": active_user,
        }
        return render(request, "web/chain.html", context)


# Handles form requests for a particular chain by redirecting to chain()
def post_chain(request):
    if not request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseRedirect(reverse("chain", kwargs={"code": request.POST['code']}))


# Displays a form to create a new "whisper chain" and handles requests to do the same
def create(request):
    if request.method == "POST":
        form = NewChainForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            maxUsers = form.cleaned_data["maxUsers"]
            length = int(maxUsers) * 2 # this could be customized later
            isPublic = form.cleaned_data["isPublic"]
            code = blake2b(str.encode(name + datetime.now().isoformat()), digest_size=int(CHAIN_CODE_LENGTH/2)).hexdigest() # pylint: disable=unexpected-keyword-arg
            chain = Chain(name=name, code=code, maxUsers=maxUsers, length=length, isPublic=isPublic)
            chain.save()
            chain.users.add(User.objects.get(username=request.user.username)) # pylint: disable=no-member
            return HttpResponseRedirect(reverse("chain", kwargs={"code": code}))

        else:
            return render(request, "web/create.html", {"form": form})

    else:
        return render(request, "web/create.html", {"form": NewChainForm()})


# Adds the user to a specified chain
def join(request):
    if request.method == "POST":
        # Took out form validation here because it wasn't recognizing the code member for some reason
        try:
            chain = Chain.objects.get(code=request.POST["code"]) # pylint: disable=no-member
        except Chain.DoesNotExist: # pylint: disable=no-member
            messages.add_message(request, messages.WARNING, f"There is no chain with the code {form.code}.") # pylint: disable=no-member
            return HttpResponseRedirect(reverse("index"))
        
        # Add the user to the chain, and close the chain if it's now got its maximum number of users
        chain.users.add(User.objects.get(username=request.user.username)) # pylint: disable=no-member
        if chain.users.all().count() >= chain.maxUsers:
            chain.isOpen = False
        chain.save()

        return HttpResponseRedirect(reverse("chain", kwargs={"code": request.POST["code"]}))
    
    else:
        return HttpResponseRedirect(reverse("index"))


# Handles user submissions of phrases and pictures to a particular chain
def submit(request, chain_code):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        chain = Chain.objects.get(code=chain_code) # pylint: disable=no-member

        # Determine if the submission is a picture or a phrase
        if "text" in request.POST:
            phrase = Phrase(user=user, chain=chain, position=chain.currentPosition, text=request.POST["text"])
            phrase.save()
            
        else:
            picture = Picture(user=user, chain=chain, position=chain.currentPosition, data=request.FILES["data"])
            picture.save()

        # Increment the chain's current position, and deactivate it (mark it finished) if it has the full number of submissions
        chain.currentPosition += 1
        if chain.currentPosition >= chain.length:
            chain.isActive = False
        chain.save()
    
    return HttpResponseRedirect(reverse("chain", kwargs={"code": chain_code}))


# Displays a credits page
def credits(request):
    return render(request, "web/credits.html", {"logged_in": request.user.is_authenticated})