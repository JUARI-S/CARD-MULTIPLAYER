from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('', views.index, name="online_28"),
    path('rules', views.rules, name="online_28_rules"),
]
