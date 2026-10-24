from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    DeckViewSet,
    CardViewSet,
    StudyView,
    StatsView,
)

router = DefaultRouter()
router.register("decks", DeckViewSet, basename="deck")
router.register("cards", CardViewSet, basename="card")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("study/", StudyView.as_view(), name="study"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("", include(router.urls)),
]