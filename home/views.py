from django.shortcuts import render, redirect

GAMES = ["Online 28"]

"""
Views for Home page
"""
def home(request):
    return render(request, "home/home.html", {
        "games": GAMES
    })


"""
Views for Profile page
"""
def profile(request):
    if request.user.is_authenticated:
        return render(request, "home/profile.html")
    return redirect("/")
