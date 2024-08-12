from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet,
    ShowSessionViewSet
)


app_name = "planetarium"

router = routers.DefaultRouter()
router.register(
    "show-theme",
    ShowThemeViewSet,
    basename="show-theme"
)
router.register(
    "astronomy-show",
    AstronomyShowViewSet,
    basename="astronomy-show"
)
router.register(
    "planetarium-dome",
    PlanetariumDomeViewSet,
    basename="planetarium-dome"
)
router.register(
    "reservation",
    ReservationViewSet,
    basename="reservation"
)
router.register(
    "show-session",
    ShowSessionViewSet,
    basename="show-session"
)

urlpatterns = [
    path("", include(router.urls))
]
