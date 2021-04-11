from django.contrib import admin
from django.urls import path
from .views import index, main, sign_in, callback, sign_out
urlpatterns = [
    path('', main, name='home'),
    path('signin', sign_in, name='signin'),
    path('signout', sign_out, name='signout'),
    path('callback', callback, name='callback'),

]
