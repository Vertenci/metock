from django.contrib.auth.models import User
from django.db import models


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    text = models.TextField('Комментарии', null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'text')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    video_file = models.FileField(upload_to='videos/', null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comments, blank=True)
    likes = models.IntegerField(default=0)
    count_views = models.IntegerField(default=True)

    def __str__(self):
        return f"Video by {self.creator.username}"

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
