from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone

from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Deck, Card
from .serializers import RegisterSerializer, DeckSerializer, CardSerializer


# Number of days before the card is due again.
INTERVALS = {
    1: 0,
    2: 1,
    3: 3,
    4: 7,
    5: 16,
}


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["subject", "is_archived"]
    search_fields = ["title"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        now = timezone.now()

        return (
            Deck.objects
            .filter(owner=self.request.user)
            .annotate(
                card_count=Count("cards", distinct=True),
                due_count=Count(
                    "cards",
                    filter=Q(cards__next_review_at__lte=now),
                    distinct=True,
                ),
            )
        )

    def perform_create(self, serializer):
        # Never trust a client-supplied owner.
        serializer.save(owner=self.request.user)


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["deck", "box"]
    search_fields = ["front", "back"]
    ordering_fields = ["created_at", "box", "next_review_at"]
    ordering = ["box", "next_review_at"]

    def get_queryset(self):
        # Ownership is checked through the deck.
        return (
            Card.objects
            .filter(deck__owner=self.request.user)
            .select_related("deck")
        )

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        card = self.get_object()

        correct = request.data.get("correct")

        # "false" as a string is not the Boolean False.
        if not isinstance(correct, bool):
            return Response(
                {
                    "correct": [
                        "This field is required and must be true or false."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()

        if correct:
            card.box = min(card.box + 1, 5)
        else:
            card.box = 1

        card.next_review_at = now + timedelta(
            days=INTERVALS[card.box]
        )
        card.last_reviewed_at = now
        card.times_reviewed += 1

        if correct:
            card.times_correct += 1

        card.save()

        return Response(CardSerializer(
            card,
            context={"request": request},
        ).data)


class StudyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        deck_id = request.query_params.get("deck")

        # An optional deck ID must belong to this user.
        if deck_id:
            deck = Deck.objects.filter(
                owner=request.user,
                pk=deck_id,
            ).first()

            if deck is None:
                return Response(
                    {"detail": "Deck not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        cards = Card.objects.filter(
            deck__owner=request.user,
            next_review_at__lte=timezone.now(),
        )

        if deck_id:
            cards = cards.filter(deck_id=deck_id)

        cards = cards.select_related("deck").order_by(
            "next_review_at"
        )[:20]

        return Response({
            "due_count": len(cards),
            "cards": CardSerializer(
                cards,
                many=True,
                context={"request": request},
            ).data,
        })


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(deck__owner=request.user)

        # Count each box in one grouped query.
        rows = cards.values("box").annotate(n=Count("id"))
        boxes = {str(i): 0 for i in range(1, 6)}

        for row in rows:
            boxes[str(row["box"])] = row["n"]

        totals = cards.aggregate(
            reviewed=Sum("times_reviewed"),
            correct=Sum("times_correct"),
        )

        reviewed = totals["reviewed"] or 0
        correct = totals["correct"] or 0

        return Response({
            "decks": Deck.objects.filter(
                owner=request.user
            ).count(),
            "cards": cards.count(),
            "due_now": cards.filter(
                next_review_at__lte=timezone.now()
            ).count(),
            "mastered": boxes["5"],
            "reviewed_today": cards.filter(
                last_reviewed_at__date=timezone.localdate()
            ).count(),
            "accuracy": (
                round(100 * correct / reviewed)
                if reviewed else 0
            ),
            "boxes": boxes,
        })