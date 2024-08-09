from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet
)

router = routers.DefaultRouter()
router.register("show_theme", ShowThemeViewSet)
router.register("astronomy_show", AstronomyShowViewSet)
router.register("planetarium_dome", PlanetariumDomeViewSet)
router.register("reservation", ReservationViewSet)


app_name = "planetarium"
urlpatterns = [
    path("", include(router.urls)),
]
