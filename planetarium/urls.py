from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet,
    ShowSessionViewSet
)

router = routers.DefaultRouter()
router.register("show_theme", ShowThemeViewSet)
router.register("astronomy_show", AstronomyShowViewSet)
router.register("planetarium_dome", PlanetariumDomeViewSet)
router.register("reservation", ReservationViewSet)
router.register("show_session", ShowSessionViewSet)

urlpatterns = [
    path("", include(router.urls))
]
app_name = "planetarium"
