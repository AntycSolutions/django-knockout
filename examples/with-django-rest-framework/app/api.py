from rest_framework import viewsets
from knockout import metadata

from app import serializers, models


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.Person.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.Task.objects.all()


class ShoppingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShoppingSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.Shopping.objects.all()
