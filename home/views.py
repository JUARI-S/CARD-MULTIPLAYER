from django.shortcuts import render

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
    return render(request, "home/profile.html")
