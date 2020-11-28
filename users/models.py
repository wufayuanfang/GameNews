from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')

    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)


class ConfirmString(models.Model):
    code = models.CharField(max_length=21)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
