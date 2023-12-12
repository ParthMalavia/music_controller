from django.db import models

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    token_type = models.CharField(max_length=50)

