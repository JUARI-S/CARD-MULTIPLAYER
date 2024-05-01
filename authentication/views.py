from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


"""
Authentication page
"""
def authentication(request):
    return render(request, "authentication/index.html")


"""
Views to Signup a new user
"""
def register(request):
    if request.method == "POST":
        username = request.POST['regUsername']
        password = request.POST['regPassword']
        confirm_pass = request.POST['confirmPassword']
        if password == confirm_pass and not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('/')
    return redirect("/auth")


"""
Views to Login a existing user
"""
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to dashboard or any other page
        else:
            messages.error(request, 'Invalid username or password.')
    return redirect("/auth")


"""
Views to logout a loggedin user
"""
def logout_user(request):
    logout(request)
    return redirect('/')
