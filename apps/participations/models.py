from django.conf import settings
from django.db import models


class Participation(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participations",
    )

    activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.CASCADE,
        related_name="participations",
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "activity"],
                name="unique_user_activity",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.activity}"
