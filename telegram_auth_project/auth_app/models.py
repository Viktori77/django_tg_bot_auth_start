from django.db import models

class AuthToken(models.Model):
    token = models.CharField(max_length=64, unique=True)
    session_key = models.CharField(max_length=64)
    is_authenticated = models.BooleanField(default=False)
    user_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)