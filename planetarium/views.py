from django.shortcuts import render
from rest_framework import mixins, viewsets

from planetarium.models import ShowTheme
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import ShowThemeSerializer


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
