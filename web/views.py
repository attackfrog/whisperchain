from django.shortcuts import render
# from django.http import HttpResponse

def index(request):
    return render(request, "web/welcome.html")

def login(request):
    return render(request, "web/login.html")

def signup(request):
    return render(request, "web/signup.html")