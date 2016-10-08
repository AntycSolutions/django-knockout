from rest_framework import viewsets
from knockout import metadata

from app import serializers, models


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.Person.objects.all()
