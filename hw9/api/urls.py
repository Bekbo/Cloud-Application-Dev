from django.contrib import admin
from django.urls import path
from .views import index, insert
urlpatterns = [
    path('', index, name='main'),
    path('post', insert, name='remove'),
]
