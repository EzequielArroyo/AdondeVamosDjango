from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    city = models.CharField(max_length=100, blank=True)

    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_complete = models.BooleanField(default=False)

    def update_completion_status(self):
        self.is_complete = all([
            self.user.first_name,
            self.user.last_name,
            self.city,
            self.bio,
        ])

    def __str__(self):
        return self.user.username
