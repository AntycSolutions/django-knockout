from django.forms import forms, models  # type: ignore
from django.db.models import base  # type: ignore

import typing


MB = typing.TypeVar('MB', bound=base.ModelBase)


def get_knockout_options(
    model_class: typing.Type[MB],
    form: models.ModelFormMetaclass
):
    ...


def get_knockout_field_options(
    field: forms.BoundField,
    knockout_fields: list,
    knockout_exclude: list,
    knockout_field_names: list,
):
    ...
