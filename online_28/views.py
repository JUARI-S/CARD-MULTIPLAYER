from django.shortcuts import render, redirect


def index(request):
    if not request.user.is_authenticated:
        return redirect('/auth')
    return render(request, 'online_28/index.html')

def rules(request):
    return render(request, 'online_28/rules.html')