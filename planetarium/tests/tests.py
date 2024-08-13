import os
import tempfile

from PIL import Image
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


def sample_planetarium_dome():
    return PlanetariumDome.objects.create(
        name="Sample Planetarium", rows=5, seats_in_row=10
    )


def image_upload_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomy-show-upload-image", kwargs={"pk": astronomy_show_id}
    )


def detail_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomy-show-detail", kwargs={"pk": astronomy_show_id}
    )


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

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "show",
            "description": "Sample description",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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


class AdminAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@example.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        theme = ShowTheme.objects.create(name="Sample Theme")
        payload = {
            "title": "show",
            "description": "Sample description",
            "show_theme": theme.id,
            "show_time": "2022-01-01 00:00:00",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_astronomy_show_wihout_theme(self):
        payload = {
            "title": "show",
            "description": "Sample description",
            "show_time": "2022-01-01 00:00:00",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_astronomy_show_without_title(self):
        theme = ShowTheme.objects.create(name="Sample Theme")
        payload = {
            "description": "Sample description",
            "show_theme": theme.id,
            "show_time": "2022-01-01 00:00:00",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_astronomy_show_without_description(self):
        theme = ShowTheme.objects.create(name="Sample Theme")
        payload = {
            "title": "show",
            "show_theme": theme.id,
            "show_time": "2022-01-01 00:00:00",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AstronomyShowImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@example.com", password="adminpass123", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.astronomy_show = sample_astronomy_show()
        self.show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=sample_planetarium_dome(),
            show_time="2022-01-01 00:00:00",
        )

    def tearDown(self):
        self.astronomy_show.image.delete()

    def test_upload_image_to_astronomy_show(self):
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (10, 10))
            img.save(image, format="JPEG")
            image.seek(0)
            payload = {"image": image}
            res = self.client.post(url, payload, format="multipart")
        self.astronomy_show.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.astronomy_show.image.path))

    def test_post_image_to_astronomy_list_should_not_work(self):
        url = ASTRONOMY_SHOW_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (10, 10))
            img.save(image, format="JPEG")
            image.seek(0)
            res = self.client.post(
                url,
                {
                    "title": "Title",
                    "description": "Description",
                    "show_theme": 1,
                    "show_time": "2022-01-01 00:00:00",
                    "image": image,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        astronomy_show = AstronomyShow.objects.get(title="Title")
        self.assertFalse(astronomy_show.image)

    def test_image_url_is_shown_on_astronomy_show_list(self):
        """Test that the image URL is shown in the list view of astronomy shows"""
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (10, 10))
            img.save(image, format="JPEG")
            image.seek(0)
            self.client.post(url, {"image": image}, format="multipart")
        res = self.client.get(ASTRONOMY_SHOW_URL)

        self.assertIn("image", res.data[0].keys())

    def test_image_url_is_shown_on_show_session_detail(self):
        """Test that the image URL is shown in the show session detail"""
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            img = Image.new("RGB", (10, 10))
            img.save(image, format="JPEG")
            image.seek(0)
            self.client.post(url, {"image": image}, format="multipart")
        res = self.client.get(SHOW_SESSION_URL)

        self.assertIn("astronomy_show", res.data[0].keys())

    def test_put_astronomy_show_not_allowed(self):
        """Test that PUT requests to the astronomy show detail are not allowed"""
        payload = {
            "title": "Updated title",
            "description": "Updated description",
            "show_theme": 1,
            "show_time": "2022-01-01 00:00:00",
        }

        astronomy_show = sample_astronomy_show()
        url = image_upload_url(astronomy_show.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_astronomy_show_not_allowed(self):
        """Test that DELETE requests to the astronomy show detail are not allowed"""
        astronomy_show = sample_astronomy_show()
        url = image_upload_url(astronomy_show.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
