from django.urls import path
from django.shortcuts import render
from . import views


urlpatterns = [
    path('', views.view_bag, name='view_bag'),
]
