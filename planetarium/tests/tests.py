from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from planetarium.models import (
    AstronomyShow,
    ShowSession,
    ShowTheme,
    PlanetariumDome,
    Ticket,
)
from planetarium.serializers import AstronomyShowSerializer

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomy-show-list")
SHOW_SESSION_URL = reverse("planetarium:show-session-list")


def sample_astronomy_show(**params):
    show_theme, _ = ShowTheme.objects.get_or_create(name="Sample theme")
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
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
            name="Sample dome", rows=10, seats_in_row=10
        ),
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def image_upload_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomical-show-upload-image", args=[astronomy_show_id]
    )


def detail_url(astronomy_show_id):
    return reverse("planetarium:astronomical-show-detail", args=[astronomy_show_id])


class UnauthenticatedAstronomicalShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_list(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomicalShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="LJQkA@example.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_shows(self):
        sample_astronomy_show()

        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_astronomy_shows_by_title(self):
        sample_astronomy_show(title="Sample show 1")
        sample_astronomy_show(title="Sample show 2")

        res = self.client.get(ASTRONOMY_SHOW_URL, {"title": "Sample show 1"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)


class PlanetariumDomeModelTests(TestCase):
    def test_capacity(self):
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10)
        self.assertEqual(dome.capacity, 50)


class TicketModelTests(TestCase):
    def test_valid_ticket(self):
        dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10)
        show = sample_astronomy_show()
        session = ShowSession.objects.create(
            astronomy_show=show, planetarium_dome=dome, show_time="2022-01-01 00:00:00"
        )
        ticket = Ticket(row=1, seat=1, show_session=session, reservation=None)
        try:
            ticket.clean()
        except ValidationError:
            self.fail("Ticket.clean() raised ValidationError unexpectedly!")


class ShowThemeViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@example.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("planetarium:show-theme-list")

    def test_list_show_themes(self):
        ShowTheme.objects.create(name="Theme 1")
        ShowTheme.objects.create(name="Theme 2")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_show_theme(self):
        payload = {"name": "Theme 1"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 1)
        self.assertEqual(ShowTheme.objects.get().name, "Theme 1")
