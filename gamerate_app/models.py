from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class VideoGame(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    rating = models.FloatField(blank=True, null=True)
    release_year = models.IntegerField()
    developer = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    review_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
