from django.db import models

class VideoGame(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    rating = models.FloatField(blank=True, null=True)
    release_year = models.IntegerField()
    developer = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title