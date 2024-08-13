from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowSession, ShowTheme, PlanetariumDome
from planetarium.serializers import AstronomyShowListSerializer

PLANETARIUM_SHOW_URL = reverse("planetarium:astronomy-show-list")
SHOW_SESSION_URL = reverse("planetarium:show-session-list")


def sample_astronomy_show(**params):
    show_theme = ShowTheme.objects.create(
        name="Sample theme"
    )
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
        "image": "image.png",
    }
    defaults.update(params)

    astronomy_show = AstronomyShow.objects.create(**defaults)
    astronomy_show.show_theme.set([show_theme])

    return astronomy_show


def sample_show_session(**params):
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "show_date": "2022-01-01 00:00:00",
        "planetarium_dome": PlanetariumDome.objects.create(
            name="Sample dome",
            rows=10,
            seats_in_row=10
        )
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def image_upload_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomical-show-upload-image",
        args=[astronomy_show_id]
    )


def detail_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomical-show-detail",
        args=[astronomy_show_id]
    )


class UnauthenticatedAstronomicalShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_list(self):
        res = self.client.get(PLANETARIUM_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomicalShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="LJQkA@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_shows(self):
        sample_astronomy_show()

        res = self.client.get(PLANETARIUM_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



