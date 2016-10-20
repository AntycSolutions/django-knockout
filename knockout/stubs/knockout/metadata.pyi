import collections

import typing

from rest_framework import metadata  # type: ignore


class KnockoutMetadata(metadata.SimpleMetadata):
    def determine_metadata(self, request, view) -> collections.OrderedDict:
        ...

    def get_serializer_info(self, serializer) -> collections.OrderedDict:
        ...

    def get_field_info(
        self, field
    ) -> typing.Tuple[collections.OrderedDict, bool]:
        ...
