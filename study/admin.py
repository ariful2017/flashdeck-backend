from django.contrib import admin
from .models import Deck, Card


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "subject",
        "is_archived",
        "created_at",
    )
    search_fields = ("title", "owner__username")
    list_filter = ("subject", "is_archived")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "front",
        "deck",
        "box",
        "next_review_at",
    )
    search_fields = ("front", "back", "deck__title")
    list_filter = ("box",)
