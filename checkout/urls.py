from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_favourites, name='view_favourites'),
]
