import json

from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User

from .utils import generate_room_id
from .models import Room


def index(request):
    if not request.user.is_authenticated:
        return redirect('/auth')
    return render(request, 'online_28/index.html')


def rules(request):
    return render(request, 'online_28/rules.html')


def create_room(request):
    if request.method == "POST" and request.user.is_authenticated:

        # Generate unique room id
        room_id = generate_room_id()

        # Fetch current user
        user = User.objects.get(username=request.user.username)

        # Create new Room object
        room = Room.objects.create(room_id=room_id, room_owner=user)
        room.team_a_players.add(user)

        return JsonResponse({
            "status": "success",
            "room_id": room_id
        })
            
    return redirect("/online_28")


def join_room(request, room_id):
    if request.method == "POST" and request.user.is_authenticated:

        # Fetch current user
        user = User.objects.get(username=request.user.username)
        
        try:
            # Fetch room from rom id
            room = Room.objects.get(room_id=room_id)

            # check if any team having space
            if room.team_a_players.count() <= 1:
                room.team_a_players.add(user)
                return JsonResponse({
                    "status": "success",
                    "message": "Team A joined"
                })
            elif room.team_b_players.count() <= 1:
                room.team_b_players.add(user)
                return JsonResponse({
                    "status": "success",
                    "message": "Team B joined"
                })
            else:
                return JsonResponse({
                    "status": "fail",
                    "message": "Room full"
                })
        except Room.DoesNotExist:
            return JsonResponse({
                "status": "fail",
                "message": "No such room exists"
            })
            
    return redirect("/online_28")


def room(request, room_id):

    if not request.user.is_authenticated:
        return redirect("/auth")

    # Fetch current user
    user = User.objects.get(username=request.user.username)

    # Retrieve room details from the database using room_id
    try:
        room = Room.objects.get(room_id=room_id)
        if room.is_player_present(user):
            return render(request, "online_28/lobby.html", {
                "room_id": room_id, 
                "username": user.username,
                "owner": room.is_room_owner(user)
            })
        else:
            return HttpResponse("You are not the part of this room", status=404)
    except Room.DoesNotExist:
        return HttpResponse("No such room exists", status=404)


def arena(request, room_id):

    if not request.user.is_authenticated:
        return redirect("/auth")

    # Fetch current user
    user = User.objects.get(username=request.user.username)

    # Retrieve room details from the database using room_id
    try:
        room = Room.objects.get(room_id=room_id)
        if room.is_player_present(user):
            if room.game_started:
                return render(request, "online_28/arena.html", {
                    "room_id": room_id, 
                    "team_name": "team_a" if room.team_a_players.filter(username=user.username).exists() else "team_b",
                    "username": user.username,
                })
            else:
                return HttpResponse("Game is not yet started for this room", status=404)
        else:
            return HttpResponse("You are not the part of this room", status=404)
    except Room.DoesNotExist:
        return HttpResponse("No such room exists", status=404)