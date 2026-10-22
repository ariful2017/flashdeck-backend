from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


class Deck(models.Model):
    class Subject(models.TextChoices):
        PROGRAMMING = "PROGRAMMING", "Programming"
        LANGUAGE = "LANGUAGE", "Language"
        ACADEMIC = "ACADEMIC", "Academic"
        INTERVIEW = "INTERVIEW", "Interview"
        OTHER = "OTHER", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decks",
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    subject = models.CharField(
        max_length=20,
        choices=Subject.choices,
        default=Subject.OTHER,
    )
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                "owner",
                name="unique_deck_title_per_owner_ci",
            ),
        ]

    def __str__(self):
        return self.title


class Card(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    front = models.TextField()
    back = models.TextField()
    hint = models.CharField(max_length=200, blank=True)
    box = models.PositiveSmallIntegerField(default=1)
    next_review_at = models.DateTimeField(default=timezone.now)
    last_reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    times_reviewed = models.PositiveIntegerField(default=0)
    times_correct = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["box", "next_review_at"]

    def __str__(self):
        return self.front[:40]
