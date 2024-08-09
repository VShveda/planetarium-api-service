from django.urls import path, include
from rest_framework import routers

from planetarium.views import ShowThemeViewSet

router = routers.DefaultRouter()
router.register("show_theme", ShowThemeViewSet)


app_name = "planetarium"
urlpatterns = [
    path("", include(router.urls)),
]
