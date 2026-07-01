from django.utils import timezone

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from .exceptions import *


class Activity(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_activities",
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="open",
    )

    location = models.CharField(max_length=255)
   
    date = models.DateTimeField()

    max_participants = models.PositiveIntegerField(
         validators=[MinValueValidator(1)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def participants_count(self):
        return self.participations.count()
    @property
    def display_status(self):
        if self.has_finished():
            return "finished"

        if self.status == "cancelled":
            return "cancelled"

        if self.status == "closed":
            return "closed"

        if not self.has_available_slots():
            return "full"

        return "open"

    def join(self, user):

        if not self.is_open():
            raise ActivityClosedError()

        if not self.has_available_slots():
            raise ActivityFullError()

        _, created = self.participations.get_or_create( user=user)

        if not created:
            raise AlreadyParticipantError()

    def leave(self, user):

        if self.has_finished():
            raise ActivityFinishedError()

        deleted_count, _ = self.participations.filter(user=user).delete()

        if deleted_count == 0:
            raise NotParticipantError()

    def has_available_slots(self):
        return (self.participants_count < self.max_participants)

    def is_open(self):
        return self.status == "open"

    def has_finished(self):
        return self.date <= timezone.now()
    
    def is_participant(self, user):
        return self.participations.filter(user=user).exists()
    
    def is_creator(self, user):
        return self.creator == user
    
    def __str__(self):
        return "activity: {}".format(self.id)