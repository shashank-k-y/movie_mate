from django.db import models

# Create your models here.


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.TextField(max_length=200)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name='watchlist')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
