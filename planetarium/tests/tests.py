from django.test import TestCase
from django.urls import reverse

PLANETARIUM_URL = reverse("planetarium:astronomical-show-list")
SHOW_SESSION_URL = reverse("planetarium:show-session-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
        "show_theme": {
            "name": "Sample theme",
        },
        "image": "image.png",
    }
    defaults.update(params)
    return defaults


def sample_show_session(**params):
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "show_date": "2022-01-01 00:00:00",
        "planetarium_dome": {
            "name": "Sample dome",
            "rows": 10,
            "seats_in_row": 10
        }
    }
    defaults.update(params)
    return defaults


def imege_upload_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomical-show-upload-image",
        args=[astronomy_show_id]
    )


def detail_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomical-show-detail",
        args=[astronomy_show_id]
    )
