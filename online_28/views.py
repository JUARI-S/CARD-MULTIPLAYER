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
    if request.method == "POST":

        # Generate unique room id
        room_id = generate_room_id()

        # Fetch current user
        user = User.objects.get(username=request.user.username)

        # Create new Room object
        room = Room.objects.create(room_id=room_id, room_owner=user)
        room.players.add(user)

        return JsonResponse({
            "status": "success",
            "room_id": room_id
        })
            
    return redirect("/online_28")


def join_room(request, room_id):
    if request.method == "POST":

        # Fetch current user
        user = User.objects.get(username=request.user.username)
        
        try:
            # Check for the room object
            room = Room.objects.get(room_id=room_id)
            if room.players_count() <= 3:
                room.players.add(user)
                return JsonResponse({
                    "status": "success",
                    "message": "Room joined"
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


def delete_room(request, room_id):
    if request.method == "POST":
        try:
            # Check for the room object
            room = Room.objects.get(room_id=room_id)
            room.delete()

            return JsonResponse({
                "status": "fail",
                "message": "Room delete successfully"
            })
        except Room.DoesNotExist:
            return JsonResponse({
                "status": "fail",
                "message": "No such room exists"
            })
            
    return redirect("/online_28")


def room(request, room_id):

    # Fetch current user
    user = User.objects.get(username=request.user.username)

    # Retrieve room details from the database using room_id
    try:
        room = Room.objects.get(room_id=room_id)
        if room.is_player_present(user):
            return render(request, "online_28/lobby.html")
        else:
            return HttpResponse("You are not the part of this room", status=404)
    except Room.DoesNotExist:
        return HttpResponse("No such room exists", status=404)


def arena(request, room_id):
    # Retrieve room details from the database using room_id
    try:
        room = Room.objects.get(pk=room_id)
        return HttpResponse(f"Room Name: {room.name}, Capacity: {room.capacity}, Location: {room.location}")
    except Room.DoesNotExist:
        return HttpResponse("Room not found", status=404)