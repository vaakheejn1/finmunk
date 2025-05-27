from django.db import models

class SavedVideo(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField()
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title