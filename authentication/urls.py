from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('login', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
]
