from django.shortcuts import render
from django.views.generic import ListView
from .models import Video


class VideosListView(ListView):
    model = Video
    template_name = 'services/home.html'
    context_object_name = 'videos'

