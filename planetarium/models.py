import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from planetarium_api_service import settings


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def astronomy_show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{instance.title}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/astronomy_shows/", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(ShowTheme)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=astronomy_show_image_file_path
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        themes = ", ".join([theme.name for theme in self.show_theme.all()])
        return f"{self.title} theme: {themes}"


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return f"{self.astronomy_show.title} {str(self.show_time)}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, planetarium_dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(
                planetarium_dome,
                planetarium_dome_attr_name
            )
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {planetarium_dome_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("show_session", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return f"{str(self.show_session)} (row: {self.row}, seat: {self.seat})"
