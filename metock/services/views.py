from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Video, Comments


class VideosListView(ListView):
    model = Video
    template_name = 'services/home.html'
    context_object_name = 'videos'

    def get_queryset(self):
        videos = super().get_queryset()
        for video in videos:
            video.count_views += 1
            video.save()
        return videos


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['description', 'video_file']
    template_name = 'services/video_create.html'
    success_url = reverse_lazy('video_view')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)
    return redirect('video_view')


@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        text = request.POST.get('text')
        if text:
            comment = Comments.objects.create(user=request.user, text=text)
            video.comments.add(comment)
        return redirect('video_view')


class VideoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['description', 'video_file']
    template_name = 'services/video_edit.html'
    success_url = reverse_lazy('video_view')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.creator


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'services/video_delete.html'
    success_url = reverse_lazy('video_view')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.creator

