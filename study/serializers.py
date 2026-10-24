from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Deck, Card

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    due_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Deck
        fields = [
            "id",
            "title",
            "description",
            "subject",
            "is_archived",
            "card_count",
            "due_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "card_count",
            "due_count",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        request = self.context["request"]

        # A title is unique for each user, ignoring capitalization.
        existing = Deck.objects.filter(
            owner=request.user,
            title__iexact=value.strip(),
        )

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError(
                "You already have a deck with this title."
            )

        return value.strip()


class CardSerializer(serializers.ModelSerializer):
    deck_title = serializers.CharField(
        source="deck.title",
        read_only=True,
    )
    is_due = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id",
            "deck",
            "deck_title",
            "front",
            "back",
            "hint",
            "box",
            "next_review_at",
            "last_reviewed_at",
            "times_reviewed",
            "times_correct",
            "is_due",
            "created_at",
            "updated_at",
        ]

        # The browser cannot manipulate the review algorithm.
        read_only_fields = [
            "id",
            "deck_title",
            "box",
            "next_review_at",
            "last_reviewed_at",
            "times_reviewed",
            "times_correct",
            "is_due",
            "created_at",
            "updated_at",
        ]

    def get_is_due(self, obj):
        return obj.next_review_at <= timezone.now()

    def validate_deck(self, deck):
        request = self.context["request"]

        if deck.owner_id != request.user.id:
            raise serializers.ValidationError(
                "This deck does not belong to you."
            )

        return deck