from django.urls import path

from . import views

urlpatterns = [
    path('login', views.clogin, name='login'),
    path('logout', views.clogout, name='logout'),
    path('register', views.registration, name='register'),
]