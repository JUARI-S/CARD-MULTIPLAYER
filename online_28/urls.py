from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('', views.index, name="online_28"),
    path('rules', views.rules, name="online_28_rules"),
    path('create_room', views.create_room, name="create_room"),
    path('join_room/<str:room_id>', views.join_room, name="join_room"),
    path('<str:room_id>', views.room, name='room'),
    path('<str:room_id>/arena', views.arena, name='arena'),
]
