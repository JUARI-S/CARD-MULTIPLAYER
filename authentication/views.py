from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


"""
Authentication page
"""
def authentication(request):
    return render(request, "authentication/index.html")


"""
Views to Signup a new user
"""
def signup(request):
    if request.method == "POST":
        # register user
        pass
    return redirect("/auth")


"""
Views to Login a existing user
"""
def login(request):
    if request.method == "POST":
        # authenticate user
        pass
    return redirect("/auth")


"""
Views to logout a loggedin user
"""
def logout_user(request):
    logout(request)
    return redirect('/')
